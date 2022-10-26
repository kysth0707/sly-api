from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from pytube import YouTube
import requests
import json
import urls
import os

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

def ReturnError(Cause, Json = None, CountA = None, CountB = None):
	if Json == None:
		return {"Status" : False, "Cause" : Cause}
	else:
		return {"Status" : False, "Cause" : Cause, "Json" : Json, "[ Count" : CountA, "] Count" : CountB}

def SearchWithSlice(FullContent, SearchKeyword, SearchNum):
	LastSearchText = 'searchVideoResultEntityKey'

	StartNum = 0
	for i in range(SearchNum):
		if FullContent.find(SearchKeyword, StartNum + 50) != -1:
			StartNum = FullContent.find(SearchKeyword, StartNum + 50) + len(SearchKeyword)
	EndNum = 0
	LastNum = -1
	for i in range(80):
		if FullContent.find(LastSearchText, EndNum + len(LastSearchText)) == -1:
			# print(f"items : {i}")
			break
		else:
			if LastNum == -1:
				EndNum = FullContent.find(LastSearchText, EndNum + 50) + len(LastSearchText)
			else:
				if LastNum - FullContent.find(LastSearchText, EndNum + 50) + len(LastSearchText) < 17000:
					EndNum = FullContent.find(LastSearchText, EndNum + 50) + len(LastSearchText)
				else:
					break
		LastNum = EndNum
		# print(i, EndNum, LastNum)
	
	EndNum = FullContent.find('"}}', EndNum) + 3
	Data = FullContent[StartNum:EndNum]
	if FullContent[EndNum + 1] != "]":
		Data = Data + "]"

	return Data


def Search(SearchText):
	Response = requests.get(f"{urls.Search}{SearchText}")
	
	# print(f"Status : {Response.status_code}")
	if Response.status_code != 200:
		return ReturnError("Youtube Request Failed")

	FullContent = str(Response.text)
	# Soup = BeautifulSoup(Response.text, 'html.parser')
	# Contents = Soup.select("#contents")

	# f = open("result.txt", "w", encoding="utf8")
	# f.write(str(Response.text))
	# f.close()

	# {\"itemSectionRenderer\":{\"contents\":

	

	# print(Data[len(Data) -500:])
	# print(EndNum)
	# Contents = FullContent[StartNum:EndNum]
	# print(Contents)
	# print(Contents.count("["))
	# print(Contents.count("]"))


	try:
		Data = SearchWithSlice(FullContent, '{\"itemSectionRenderer\":{\"contents\":', 1)
		Contents = json.loads(Data)
	except Exception as e:
		# print(e)
		try:
			Data = SearchWithSlice(FullContent, '{\"itemSectionRenderer\":{\"contents\":', 10)
			Contents = json.loads(Data)

		except Exception as e:
			return ReturnError("Json Parse Failed", Data, Data.count("["), Data.count("]"))

	Export = []
	for i in range(len(Contents)):
		try:
			# print(Contents[0])
			VideoID = (Contents[i]['videoRenderer']['videoId']) #ID
			ThumbnailLow = (Contents[i]['videoRenderer']['thumbnail']['thumbnails'][0]['url']) #LOW QUALITY
			ThumbnailHigh = (Contents[i]['videoRenderer']['thumbnail']['thumbnails'][1]['url']) #HIGH QUALITY
			Title = (Contents[i]['videoRenderer']['title']['runs'][0]['text']) # 제목
			ViewFull = (Contents[i]['videoRenderer']['viewCountText']['simpleText']) # 조회수
			ViewShort = (Contents[i]['videoRenderer']['shortViewCountText']['simpleText']) # 조회수 간단
			VideoLength = (Contents[i]['videoRenderer']['lengthText']['accessibility']['accessibilityData']['label']) # 길이
			PublishTime = (Contents[i]['videoRenderer']['publishedTimeText']['simpleText']) # 올려진 시간
			Owner = (Contents[i]['videoRenderer']['ownerText']['runs'][0]['text']) # 게시자 이름
			OwnerLink = (Contents[i]['videoRenderer']['ownerText']['runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']) # 게시자 채널링크
			OwnerPictureLink = (Contents[i]['videoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url']) # 게시자 채널 사진
			# print(Contents[0]['videoRenderer']['channelThumbnailSupportedRenderers'])

			Dict = {}
			Dict['VideoID'] = VideoID
			Dict['ThumbnailLow'] = ThumbnailLow
			Dict['ThumbnailHigh'] = ThumbnailHigh
			Dict['Title'] = Title
			Dict['ViewFull'] = ViewFull
			Dict['ViewShort'] = ViewShort
			Dict['VideoLength'] = VideoLength
			Dict['PublishTime'] = PublishTime
			Dict['Owner'] = Owner
			Dict['OwnerLink'] = OwnerLink
			Dict['OwnerPictureLink'] = OwnerPictureLink
			# print(Dict)
			Export.append(Dict)
		except:
			pass
			# print("영상 아님")
		# print("==========================")

	# f = open("result.txt", "w", encoding="utf8")
	# f.write(str(Response.text))
	# f.close()

	return Export

def MP3Download(VideoID):
	if os.path.isfile(f"./mp3/{VideoID}.mp3"):
		return FileResponse(f"./mp3/{VideoID}.mp3")
	try:
		yt = YouTube(f"https://www.youtube.com/watch?v={VideoID}")
		yt.streams.filter(only_audio=True).first().download('./mp3',filename=f"{VideoID}.mp3")
		return FileResponse(f"./mp3/{VideoID}.mp3")
	except:
		return False
	# https://www.youtube.com/watch?v=Wi17ybKXmXE

def SearchWithSlice2(FullContent, SearchKeyword):
	Start = FullContent.find(SearchKeyword) + len(SearchKeyword)
	a=[]
	End = 0
	WaitFlag = False
	for i in range(Start-1, 10000000):
		if FullContent[i] == "[":
			WaitFlag = True
			a.append(True)
		elif FullContent[i] == "]":
			a.pop()
		if len(a) == 0 and WaitFlag:
			End = i
			break
	return FullContent[Start:End + 1]

def VideoList(url):
	Response = requests.get(url)
	FullContent = str(Response.text)
	
	# if Response.status_code != 200:
	# 	return ReturnError("Youtube Request Failed")

	Data = SearchWithSlice2(FullContent, ',"content":{"sectionListRenderer":{"contents":')

	f = open("result.txt", "w", encoding="utf8")
	f.write(Data)
	f.close()

	Contents = json.loads(Data)
	Contents = Contents[0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items']
	# print(Contents[0]['gridVideoRenderer']['videoId'])
	# print(Contents[0]['gridVideoRenderer']['thumbnail']['thumbnails'][0]['url'])
	# print(Contents[0]['gridVideoRenderer']['title']['runs'][0]['text'])
	# print(Contents[0]['gridVideoRenderer']['publishedTimeText']['simpleText'])
	# print(Contents[0]['gridVideoRenderer']['shortViewCountText']['accessibility']['accessibilityData']['label'])
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
	return ReturnValue

@app.get('/')
def a():
	return "Hello, world!"

@app.get('/get/{text}/')
def b(text, request : Request):
	# print(request.client.host)
	return Search(text)

@app.get('/mp3/{url}')
def c(url, request : Request):
	return MP3Download(url)

@app.get('/videos/{url}')
def d(url, request : Request):
	return VideoList(f"https://www.youtube.com/user/{url}/videos")

if __name__ == "__main__":
	uvicorn.run("app:app", host="0.0.0.0", port=7070, reload=True)