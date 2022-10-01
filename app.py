from urllib.error import ContentTooShortError
import requests
from bs4 import BeautifulSoup
import urls
import json


class slyAPI:
	def __init__(self) -> None:
		pass

	def Search(self, SearchText):
		Response = requests.get(f"{urls.Search}{SearchText}")
		
		print(f"Status : {Response.status_code}")
		FullContent = str(Response.text)
		# Soup = BeautifulSoup(Response.text, 'html.parser')
		# Contents = Soup.select("#contents")

		StartNum = FullContent.find('[{"itemSectionRenderer":{"contents":') + len('[{"itemSectionRenderer":{"contents":')
		EndNum = 0
		for i in range(50):
			if FullContent.find('"searchVideoResultEntityKey":"', EndNum + 50) == -1:
				print(f"items : {i}")
				break
			else:
				EndNum = FullContent.find('"searchVideoResultEntityKey":"', EndNum + 50) + 50
		EndNum = FullContent.find('"}}],', EndNum) + 4
		Contents = FullContent[StartNum:EndNum]
		# print(Contents)
		# print(Contents.count("["))
		# print(Contents.count("]"))
		Contents = json.loads(FullContent[StartNum:EndNum])
		try:
			# print(Contents[0])
			print(Contents[0]['videoRenderer']['videoId']) #ID
			print(Contents[0]['videoRenderer']['thumbnail']['thumbnails'][0]['url']) #LOW QUALITY
			print(Contents[0]['videoRenderer']['thumbnail']['thumbnails'][1]['url']) #HIGH QUALITY
			print(Contents[0]['videoRenderer']['title']['runs'][0]['text']) # 제목
			print(Contents[0]['videoRenderer']['viewCountText']['simpleText']) # 조회수
			print(Contents[0]['videoRenderer']['shortViewCountText']['simpleText']) # 조회수 간단
			print(Contents[0]['videoRenderer']['lengthText']['accessibility']['accessibilityData']['label']) # 길이
			print(Contents[0]['videoRenderer']['publishedTimeText']['simpleText']) # 올려진 시간
			print(Contents[0]['videoRenderer']['ownerText']['runs'][0]['text']) # 게시자 이름
			print(Contents[0]['videoRenderer']['ownerText']['runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']) # 게시자 채널링크
			print(Contents[0]['videoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url']) # 게시자 채널 사진
			# print(Contents[0]['videoRenderer']['channelThumbnailSupportedRenderers'])
		except:
			print("영상 아님")

		# f = open("result.txt", "w", encoding="utf8")
		# f.write(str(Response.text))
		# f.close()

a = slyAPI()
a.Search('사이렌')