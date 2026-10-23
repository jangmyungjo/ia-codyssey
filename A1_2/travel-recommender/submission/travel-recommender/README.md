# 국내 여행 추천 CLI

여행 날짜를 입력하면 Codyssey를 통해 호출한 LLM이 국내 여행지를 JSON으로 추천하고, 네이버 지역 검색 API가 해당 지역의 음식점을 최대 5곳 검색합니다. 두 결과를 다시 LLM에 전달하여 Markdown 여행 리포트를 생성합니다. 맛집 검색 결과는 검색 순서이며 평점 순위나 품질 보증이 아닙니다.

## 설치

Python 3.9 이상에서 프로젝트 폴더로 이동하여 실행합니다. 표준 라이브러리만 사용하므로 별도 패키지 설치는 필요하지 않습니다.

```bash
cd travel-recommender
python3 -m venv .venv
source .venv/bin/activate
cp .env.example .env
```

Windows에서는 가상환경 활성화 명령으로 `.venv\Scripts\activate`를 사용합니다.

## API 키 설정

`.env`를 편집하여 다음 항목에 실제 키를 입력하세요. 키를 채팅으로 보내지 마세요.

```dotenv
CODYSSEY_API_KEY=your_codyssey_virtual_key
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret
CODYSSEY_MODEL=gpt-5-mini
```

- Codyssey: [API 콘솔](https://usr.codyssey.kr/public-api-console)에서 확인한 가상 키(virtual key)를 `CODYSSEY_API_KEY`에 입력합니다. 요청 주소는 `https://copa.codyssey.kr/v1/chat/completions`이며, `Authorization: Bearer <virtual-key>` 헤더로 인증합니다. 기본 모델은 제공된 호출 예제의 `gpt-5-mini`입니다.
- 네이버: 네이버 클라우드 콘솔의 **NAVER API HUB → Application**에서 검색 API를 선택한 앱의 Client ID/Secret을 설정합니다. 기존 `NAVER_CLIENT_ID`와 `NAVER_CLIENT_SECRET` 변수명을 그대로 사용합니다. 요청 헤더는 `X-NCP-APIGW-API-KEY-ID`와 `X-NCP-APIGW-API-KEY`이며, 요청 주소는 `https://naverapihub.apigw.ntruss.com/search/v1/local`입니다. 기존 Developers Center의 인증 정보와는 호환되지 않습니다. 401이면 인증 정보와 앱의 API 권한을 확인하세요.
- 환경변수로 설정해도 됩니다. 기존 환경변수는 `.env`보다 우선합니다. `.env`는 한 줄에 `KEY=값` 형식이며 따옴표를 지원합니다. 변수 치환과 여러 줄 값은 지원하지 않습니다. 모델은 Codyssey에서 사용 가능한 모델로 변경할 수 있습니다. JSON 전용 옵션 지원은 확인되지 않아 프롬프트로 JSON을 요청하고 코드에서 파싱·타입 검증 및 1회 재시도합니다.
- 키가 없으면 API를 호출하기 전에 종료합니다. 401/403은 키 종류, 값, 권한 및 헤더 설정을 확인하세요.

## 실행

```bash
python main.py -date "2026-11-14"
python main.py --help
```

`-date`는 필수입니다. `2026-02-30`, `2026-1-1`처럼 잘못된 날짜는 사용법을 출력하고 종료 코드 2로 종료합니다. 정상 실행은 진행 로그와 저장 경로를 출력합니다.

## 결과 확인

프로젝트의 `results/` 폴더가 자동 생성됩니다. 파일명은 여행일이 아닌 **컴퓨터의 현지 실행일과 시각** 기준이며, 반복 실행 시 덮어쓰지 않습니다.

```text
results/travel_2026-10-24_143000_123456.json
results/travel_2026-10-24_143000_123456.md
```

JSON에는 `travel_date`, `executed_at`, `recommendation`(도시·날씨·행사·추천 이유), `restaurants`(이름·주소·분류·URL·숫자 좌표 — 네이버 mapx/mapy 원본 값을 x/y로 보존), `errors`가 포함됩니다. Markdown에는 필수 정보와 AI 종합 제안, 오류 요약이 들어갑니다.

## 오류 처리와 한계

- 추천 JSON의 형식 또는 필수 필드가 잘못되면 1회 재요청합니다. 두 번 모두 실패하면 진단용 JSON/Markdown을 저장하고 종료 코드 1로 끝납니다. 이 경우 `recommendation`은 `null`입니다.
- 지도 API 실패 또는 0건이면 빈 맛집 목록과 “데이터 없음”으로 계속 진행합니다. API 실패 내용은 `errors`에 남깁니다.
- 최종 LLM 호출이 실패해도 수집 데이터로 기본 리포트를 저장합니다.
- 날씨는 실시간 예보가 아닌 계절 경향입니다. 행사/축제는 후보이며 실제 개최 여부와 영업시간을 방문 전 확인하세요.
- 네트워크 요청 제한 시간은 호출당 60초입니다. API 사용료가 발생할 수 있습니다.

## 검증

```bash
python -m unittest discover -s tests -v
```

자동 테스트는 가짜 API 응답으로 정상 흐름, 재시도, 지도 오류, 0건, 최종 생성 실패, 키 누락, 날짜 검증 및 파일 저장을 확인합니다. 실제 API 연동은 본인의 키를 설정한 뒤 위 실행 명령으로 확인하세요. 테스트 결과는 실제 API 실행 증빙이 아닙니다.

## 보안

`.env`와 `results/`는 Git 제외 대상입니다. 제출할 결과 JSON/Markdown은 직접 검토한 뒤 필요한 파일만 첨부하세요. 코드, README, 터미널 캡처 및 로그에 실제 키를 넣지 마세요. 유출 시 제공자 콘솔에서 키를 폐기하고 재발급하세요. 프로그램은 요청 헤더나 API 오류 응답 본문을 로그에 출력하지 않습니다.

## 참고 문서

- [Codyssey API 콘솔](https://usr.codyssey.kr/public-api-console) — 제공된 Python 호출 예제를 기준으로 연동
- [NAVER API HUB 지역 검색 API](https://api.ncloud-docs.com/docs/naver-api-hub-search-local)
