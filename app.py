from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
import uvicorn

import requests
import json
import urls

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
def Search(SearchText):
	Response = requests.get(f"{urls.Search}{SearchText}")
	
	# print(f"Status : {Response.status_code}")
	if Response.status_code != 200:
		return False
	FullContent = str(Response.text)
	# Soup = BeautifulSoup(Response.text, 'html.parser')
	# Contents = Soup.select("#contents")

	StartNum = FullContent.find('[{"itemSectionRenderer":{"contents":') + len('[{"itemSectionRenderer":{"contents":')
	EndNum = 0
	for i in range(50):
		if FullContent.find('"searchVideoResultEntityKey":"', EndNum + 50) == -1:
			# print(f"items : {i}")
			break
		else:
			EndNum = FullContent.find('"searchVideoResultEntityKey":"', EndNum + 50) + 50
	EndNum = FullContent.find('"}}],', EndNum) + 4
	Contents = FullContent[StartNum:EndNum]
	# print(Contents)
	# print(Contents.count("["))
	# print(Contents.count("]"))
	Contents = json.loads(FullContent[StartNum:EndNum])

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

@app.get('/')
def a():
	return "Hello, world!"

@app.get('/get/{text}/')
def b(text, request : Request):
	print(request.client.host)
	return Search(text)

if __name__ == "__main__":
	uvicorn.run("app:app", host="0.0.0.0", port=7070, reload=True)