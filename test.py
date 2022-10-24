import requests
import json
import urls

url="https://www.youtube.com/user/woowakgood/videos"

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

def VideoList():
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
	for i in range(len(Contents)):
		try:
			print(Contents[i]['gridVideoRenderer']['title']['runs'][0]['text'])
			print(Contents[i]['gridVideoRenderer']['thumbnail']['thumbnails'][0]['url'])
			print("====================")
		except:
			pass


VideoList()