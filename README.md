sly 전용 API 서버

기능들 ( 제작 완료 )
- 유튜브 검색
- 유튜브 검색 기반 썸네일 , 링크
- 유튜브 검색 기반 채널 사진 , 링크

사용법
1. 해당 py 파일을 실행한다
2. localhost:7070 에 서버가 열리게 된다.
3. localhost:7070/get/검색어/ 로 검색이 가능하다. 단 / 는 사용이 불가능하다

중요한 점
- 유튜브 검색 방식 변경 시, 사용 불가
해당 API 를 Request 기반 이여서 유튜브 검색 방식이 바뀌면 사용이 불가능합니다
언제 바뀔 지 어떻게 바뀔 지 전혀 모릅니다

- 제한 없음
YOUTUBE DATA API V3 에서는 검색이 1일 100회 였던 반면에,
이 API 는 Request 기반이여서 제한이 없습니다.

- 선택적 영상 검색
검색어 : 안녕 / 선택 : 실시간
https://www.youtube.com/results?search_query=안녕&sp=EgJAAQ%253D%253D

이런 식으로 검색하시고 싶으시면, urls.py 를 변경해주셔야합니다.
단, search_query= 가 반드시 마지막에 올 수 있도록 해주세요
[ O ] https://www.youtube.com/results?sp=EgJAAQ%253D%253D&search_query=안녕
[ X ] https://www.youtube.com/results?search_query=안녕&sp=EgJAAQ%253D%253D