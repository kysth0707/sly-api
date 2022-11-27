import json

with open('result.txt', 'w', encoding="utf-8") as f:
	json.dump(json.loads(input()), f, ensure_ascii=False, indent=4)
