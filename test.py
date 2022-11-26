import requests
import json
import urls

url="https://www.youtube.com/watch?v=fgSXAKsq-Vo"

Response = requests.get(url)

if Response.status_code != 200:
	print("Youtube Request Failed")

def Slice(Content, Slice):
	Content = Content[Content.find(Slice) + len(Slice):]
	Count = 0
	for i in range(100000):
		if Content[i] == "[":
			Count += 1
		elif Content[i] == "]":
			Count -= 1
			if Count == 0:
				return Content[:i+1]


FullContent = str(Response.text)
FullContent = Slice(FullContent,'{"results":{"contents":')

FullContent = json.loads(FullContent)
FullContent = FullContent[0]['videoPrimaryInfoRenderer']
print(f"제목 : {FullContent['title']['runs'][0]['text']}")
ViewCount = str(FullContent['viewCount']['videoViewCountRenderer']['viewCount']['simpleText'])
ViewCount = int(ViewCount.split(' ')[1].replace(',','').replace('회',''))
print(f"조회수 : {ViewCount}")
LikeCount = FullContent['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']
LikeCount = int(LikeCount.split(' ')[1].replace(',','').replace('개',''))
print(f"좋아요 : {LikeCount}")
OpenDate = str(FullContent['dateText']['simpleText']).replace('최초 공개: ','').replace('.','')
print(f"공개일 : {OpenDate}")

with open('result.txt', 'w', encoding="utf-8") as f:
	json.dump(FullContent, f, ensure_ascii=False, indent=4)
