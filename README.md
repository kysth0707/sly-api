sly 전용 API 서버

필요 라이브러리
- FastAPI
- requests
- uvicorn

기능들 ( 제작 완료 )
- 유튜브 검색
- 유튜브 검색 기반 썸네일 , 링크
- 유튜브 검색 기반 채널 사진 , 링크

사용법
1. 해당 py 파일을 실행한다
2. localhost:7070 에 서버가 열리게 된다.
3. localhost:7070/get/검색어/ 로 검색이 가능하다. 단 / 는 사용이 불가능하다

Return Value
- VideoID : 영상 아이디 ex)JsYQmJfklfk
- ThumbnailLow : 저화질 썸네일 ex)https://i.ytimg.com ...
- ThumbnailHigh : 고화질 썸네일 ex)https://i.ytimg.com ...
- Title : 제목 ex)세계가 놀라고...
- ViewFull : 총 조회수 ex)조회수 1,242,290회
- ViewShort : 총 조회수 ex)조회수 124만회
- VideoLength : 영상 길이 ex)10분 13초
- PublishTime : 영상 게시일 ex)3년 전
- Owner : 영상 게시자 ex)샌즈마크언더테일...
- OwnerLink : 영상 게시자 주소 ex)/c/샌즈마크...
- OwnerPictureLink : 영상 게시자 사진 ex)https://yt3.ggpht.com ...

Fail Value
- {"Status":false,"Cause":"Json Parse Failed"} : Json 파싱 실패, 코드 내 문제입니다 ( 해결 방안 찾는 중 )
- {"Status":false,"Cause":"Youtube Request Failed"} 유튜브 연결 실패, 아마 유튜브 문제입니다

중요한 점
> 유튜브 검색 방식 변경 시, 사용 불가
- 해당 API 를 Request 기반 이여서 유튜브 검색 방식이 바뀌면 사용이 불가능합니다
- 언제 바뀔 지 어떻게 바뀔 지 전혀 모릅니다

> 제한 없음
- YOUTUBE DATA API V3 에서는 검색이 1일 100회 였던 반면에,
- 이 API 는 Request 기반이여서 제한이 없습니다.

> 선택적 영상 검색
- 검색어 : 안녕 / 선택 : 실시간
- https://www.youtube.com/results?search_query=안녕&sp=EgJAAQ%253D%253D

이런 식으로 검색하시고 싶으시면, urls.py 를 변경해주셔야합니다.
> 단, search_query= 가 반드시 마지막에 올 수 있도록 해주세요
- [ O ] https://www.youtube.com/results?sp=EgJAAQ%253D%253D&search_query=
- [ X ] https://www.youtube.com/results?search_query=&sp=EgJAAQ%253D%253D