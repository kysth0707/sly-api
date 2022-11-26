from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
# from pytube import YouTube
import requests
import json
import urls
# import os

app = FastAPI()

origins = [
	"*"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

def ReturnError(Cause):
	return {"Status" : False, "Cause" : Cause}

def Slice(Content, SliceText):
	SliceTextLoc = Content.find(SliceText)
	Content = Content[Content.find("[", SliceTextLoc):]
	Count = 0
	for i in range(1000000):
		if Content[i] == "[":
			Count += 1
		elif Content[i] == "]":
			Count -= 1
			if Count == 0:
				return Content[:i+1]


def Search(SearchText):
	Response = requests.get(f"{urls.Search}{SearchText}")
	
	# print(f"Status : {Response.status_code}")
	if Response.status_code != 200:
		return ReturnError("Youtube Request Failed")

	FullContent = str(Response.text)

	Data = str(Slice(FullContent, '{\"itemSectionRenderer\":{\"contents\":'))
	Contents = json.loads(Data)

	ReturnData = {'Status' : True}
	Export = []
	for i in range(len(Contents)):
		try:
			Content = Contents[i]['videoRenderer']
			# print(Contents[0])
			VideoID = (Content['videoId']) #ID
			ThumbnailLow = (Content['thumbnail']['thumbnails'][0]['url']) #LOW QUALITY
			ThumbnailHigh = (Content['thumbnail']['thumbnails'][1]['url']) #HIGH QUALITY
			Title = (Content['title']['runs'][0]['text']) # 제목
			ViewFull = (Content['viewCountText']['simpleText']) # 조회수
			ViewShort = (Content['shortViewCountText']['simpleText']) # 조회수 간단
			VideoLength = (Content['lengthText']['accessibility']['accessibilityData']['label']) # 길이
			PublishTime = (Content['publishedTimeText']['simpleText']) # 올려진 시간
			Owner = (Content['ownerText']['runs'][0]['text']) # 게시자 이름
			OwnerLink = (Content['ownerText']['runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']) # 게시자 채널링크
			OwnerPictureLink = (Content['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url']) # 게시자 채널 사진
			
			Export.append({
				'VideoID' : VideoID,
				'ThumbnailLow' : ThumbnailLow,
				'ThumbnailHigh' : ThumbnailHigh,
				'Title' : Title,
				'ViewFull' : ViewFull,
				'ViewShort' : ViewShort,
				'VideoLength' : VideoLength,
				'PublishTime' : PublishTime,
				'Owner' : Owner,
				'OwnerLink' : OwnerLink,
				'OwnerPictureLink' : OwnerPictureLink
			})
		except:
			pass
	
	ReturnData['Data'] = Export
	return ReturnData

# def MP3Download(VideoID):
# 	if os.path.isfile(f"./mp3/{VideoID}.mp3"):
# 		return FileResponse(f"./mp3/{VideoID}.mp3")
# 	try:
# 		yt = YouTube(f"https://www.youtube.com/watch?v={VideoID}")
# 		yt.streams.filter(only_audio=True).first().download('./mp3',filename=f"{VideoID}.mp3")
# 		return FileResponse(f"./mp3/{VideoID}.mp3")
# 	except:
# 		return False

def VideoList(url):
	Response = requests.get(url)
	FullContent = str(Response.text)

	Data = Slice(FullContent, ',"content":{"sectionListRenderer":{"contents":')

	Contents = json.loads(Data)
	Contents = Contents[0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items']
	ReturnData = {'Status' : True}
	ReturnValue=[]
	for i in range(len(Contents)):
		try:
			ReturnValue.append({"Title":Contents[i]['gridVideoRenderer']['title']['runs'][0]['text'],
								"Thumnail":Contents[i]['gridVideoRenderer']['thumbnail']['thumbnails'][0]['url'],
								"VideoID":Contents[0]['gridVideoRenderer']['videoId'],
								"Date":Contents[0]['gridVideoRenderer']['publishedTimeText']['simpleText'],
								"ViewCount":Contents[0]['gridVideoRenderer']['shortViewCountText']['accessibility']['accessibilityData']['label']
								})
		except:
			pass
	ReturnData['Data'] = ReturnValue
	return ReturnData

def GetVideoData(ID):
	url = f"https://www.youtube.com/watch?v={ID}"

	Response = requests.get(url)

	if Response.status_code != 200:
		return ReturnError("Youtube Request Failed")

	FullContent = str(Response.text)
	FullContent = Slice(FullContent,'{"results":{"contents":')

	FullContent = json.loads(FullContent)
	FullContent = FullContent[0]['videoPrimaryInfoRenderer']
	
	Title = FullContent['title']['runs'][0]['text']

	ViewCount = str(FullContent['viewCount']['videoViewCountRenderer']['viewCount']['simpleText'])
	ViewCount = int(ViewCount.split(' ')[1].replace(',','').replace('회',''))
	
	LikeCount = FullContent['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']
	LikeCount = int(LikeCount.split(' ')[1].replace(',','').replace('개',''))
	
	PublishDate = str(FullContent['dateText']['simpleText']).replace('최초 공개: ','').replace(' ','')

	return {
		'Status' : True,
		'Title' : Title,
		'ViewCount' : ViewCount,
		'LikeCount' : LikeCount,
		'PublishDate' : PublishDate
	}

@app.get('/')
def a():
	return "Hello, world!"

@app.get('/get/{text}/')
def b(text, request : Request):
	# print(request.client.host)
	try:
		return Search(text)
	except Exception as e:
		return ReturnError(str(e))

# @app.get('/mp3/{url}')
# def c(url, request : Request):
# 	return MP3Download(url)

@app.get('/channelvideo/{url}')
def d(url, request : Request):
	try:
		return VideoList(f"https://www.youtube.com/{url}/videos")
	except Exception as e:
		return ReturnError(str(e))
# https://www.youtube.com/@waktaverse/videos

@app.get('/video/{ID}')
def e(ID, request : Request):
	try:
		return GetVideoData(ID)
	except Exception as e:
		return ReturnError(str(e))

if __name__ == "__main__":
	uvicorn.run("app:app", host="0.0.0.0", port=7070, reload=True)