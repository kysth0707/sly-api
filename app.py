import requests
from bs4 import BeautifulSoup
import urls


class slyAPI:
	def __init__(self) -> None:
		pass

	def Search(self, SearchText):
		Response = requests.get(f"{urls.Search}{SearchText}")
		print(Response.status_code)
		Soup = BeautifulSoup(Response.text, 'html.parser')
		
		Contents = Soup.select("#contents")
		print(Contents)

a = slyAPI()
a.Search('리스빈')