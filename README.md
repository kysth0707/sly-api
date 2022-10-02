# Youtube Search API ( No Limit ) / 유튜브 검색 API ( 제한 없음 )
EN / KR

# Libraries / 라이브러리
- FastAPI
- requests
- uvicorn

# Functions / 기능들
- Youtube Search / 유튜브 검색
- YouTube search-based Datas. ( please check 'Return Value' ) / 유튜브 검색 기반 데이터들 ( 'Return Value' 를 확인해주세요 )

# How to use / 사용법
1. RUN app.py / app.py 실행
2. Then, server will open in localhost:7070 / 그러면 localhost:7070 에 서버가 열릴 것 입니다.
3. You can search youtube by localhost:7070/get/SEARCH KEYWORD/   |   localhost:7070/get/검색어/ 로 검색이 가능합니다.
- But, '/' can't be used in SEARCH KEYWORD / 단, '/' 는 검색어로 사용이 불가능합니다.

# Returned Value / 반환 값
> KEY : EN / KR ex)Example
- VideoID : VideoID / 영상 아이디 ex)JsYQmJfklfk
- ThumbnailLow : Low Quality Thumbnail / 저화질 썸네일 ex)https://i.ytimg.com ...
- ThumbnailHigh : High Quality Thumbnail / 고화질 썸네일 ex)https://i.ytimg.com ...
- Title : Title / 제목 ex)세계가 놀라고...
- ViewFull : View Full Text / 총 조회수 ex)조회수 1,242,290회
- ViewShort : View Short Text / 간단한 조회수 ex)조회수 124만회
- VideoLength : Video Length / 영상 길이 ex)10분 13초
- PublishTime : Published Time / 영상 게시일 ex)3년 전
- Owner : Owner / 영상 게시자 ex)샌즈마크언더테일...
- OwnerLink : Owner Link / 영상 게시자 주소 ex)/c/샌즈마크...
- OwnerPictureLink : Owner Picture Link / 영상 게시자 사진 ex)https://yt3.ggpht.com ...

# Fail Value / 실패 값
> {"Status" : False, "Cause" : Cause, "Json" : Json, "[ Count" : CountA, "] Count" : CountB}
- Json parsing failed. If this error cause, please open issue! ^v^
- Json 파싱 실패, 이 오류가 생기면 Issue 에 남겨주세요! ^v^
> {"Status":false,"Cause":"Youtube Request Failed"}
- Failed to get data from YouTube, Maybe.. It's Youtube's problem.
- 유튜브 연결 실패, 아마 유튜브 문제입니다

# Note / 읽어주세요
- If youtube changes search format or return json, this can't be used. ( If this cause, please open issue! ^v^ )
- 유튜브 검색 방식 또는 반환 Json 이 변경되었을 시, 사용 불가 ( 이게 발생되면, issue 를 열어주세요! ^v^ )

- No Limit  
 YOUTUBE DATA API V3 : 100 search / 1 day  
 This : No Limit / 1 day  
 YOUTUBE DATA API V3 : 1 일 100 검색  
 This : 1 일 제한 없음.  

# Selective video search / 선택적 영상 검색
> Query: Hello / Select: Realtime | 검색어 : 안녕 / 선택 : 실시간
- https://www.youtube.com/results?search_query=Hello&sp=EgJAAQ%253D%253D
- https://www.youtube.com/results?search_query=안녕&sp=EgJAAQ%253D%253D
  
You need to change urls.py. / urls.py 를 변경해야합니다.  
> However, make sure that search_query= comes last.  
> 단, search_query= 가 반드시 마지막에 올 수 있도록 해주세요  
- [ O ] https://www.youtube.com/results?sp=EgJAAQ%253D%253D&search_query=
- [ X ] https://www.youtube.com/results?search_query=&sp=EgJAAQ%253D%253D