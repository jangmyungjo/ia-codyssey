# [과제 제출용] 구글 & Runway 무료 플랜 기반 AI 광고 기획서

## 1. 브랜드 아이덴티티 및 캠페인 정의

* **브랜드명 / 슬로건**: 나이키 (NIKE) / JUST DO IT.
* **타겟**: 매일 밤 도심을 달리는 트렌디한 시티 러너(City Runner) 및 2030 런크루
* **톤앤매너**: 시네마틱, 네온, 역동적, 어두운 도심 속 강렬한 빛의 대비
* **USP (차별점)**: 야간 러닝 시 빛을 반사하는 네온 리플렉티브 소재와 압도적인 쿠셔닝의 비주얼화
* **캠페인 목적**: 야간 러닝화 신제품 론칭 및 브랜드 슬로건 재각인
* **핵심 메시지**: "어둠이 깊어질수록, 너의 움직임은 선명해진다."

---

## 2. 씬별 스토리보드 (구글 무료 + Runway 무료 플랜 파이프라인)
> **총 길이 9초** (3개 씬 × 각 3초) 구성으로, Runway 무료 크레딧 소모를 최소화합니다.

### 🎬 씬 1 (Intro: 무드 형성)
* **씬 번호 / 길이**: #1 / 3초
* **목표 메시지**: 밤의 도심과 러닝이 시작되기 직전의 긴장감 연출
* **화면 구성**: 밤의 서울 도심, 비에 젖어 가로등과 네온사인이 은은하게 반사되는 아스팔트 도로 앵글 (인물 없음)
* **내레이션/카피**: (화면 카피) "모두가 잠든 밤,"
* **사용 도구 및 목적**:
  * **이미지 생성**: 구글 Gemini (Imagen 3 무료) ➡️ 고화질의 시네마틱한 야간 도시 배경 이미지를 비용 없이 확보하기 위해 사용.
  * **비디오 변환**: Runway Gen-2 / Gen-3 (무료 플랜) ➡️ [Image-to-Video] 기능 활용. Gemini가 만든 정지 이미지를 입력하고 카메라 무빙을 주어 생동감 있는 3초 영상으로 변환.
* **입력 프롬프트**:
  * **Gemini (이미지)**: `Cinematic side angle shot of a wet asphalt road at night in Seoul, neon signs and streetlights reflecting on the puddles, blurry cityscape background, moody and cyber aesthetics, 8k, photorealistic, aspect ratio 16:9`
  * **Runway (비디오)**: `Slow camera low-angle tracking shot, soft neon light reflections moving naturally on the wet ground`
* **출력 결과 요약**: 어둡고 트렌디한 야간 도시의 감성이 움직임으로 표현된 3초 비디오 확보
* **결과 파일명**: `Nike_scene01_Gemini.png` / `Nike_scene01_Runway.mp4`

### 🎬 씬 2 (Body: 제품 등장 - 핵심 클로즈업)
* **씬 번호 / 길이**: #2 / 3초
* **목표 메시지**: 나이키 운동화의 역동적인 성능과 강렬한 비주얼 전달
* **화면 구성**: 밤의 도로를 힘차게 달리는 러너의 발 클로즈업 숏. 발이 지면을 차고 나갈 때 운동화 옆면의 나이키 스우시(Swoosh) 로고가 네온 컬러로 강렬하게 빛남.
* **내레이션/카피**: (화면 카피) "너만의 빛으로 달려라."
* **사용 도구 및 목적**:
  * **이미지 생성**: 구글 Gemini (Imagen 3 무료) ➡️ 달리는 발의 역동적인 순간과 운동화 디테일을 무료로 정교하게 표현하기 위해 사용.
  * **비디오 변환**: Runway (무료 플랜) ➡️ [Image-to-Video] 기능 활용. 고정된 운동화 이미지에 강렬한 앞방향 추진력과 지면의 역동적인 모션을 부여하기 위해 사용.
* **입력 프롬프트**:
  * **Gemini (이미지)**: `Extreme close-up macro shot of a runner's feet sprinting on a city street at night, wearing futuristic black Nike running shoes with a glowing neon orange swoosh logo, dynamic motion blur, hyper-realistic fabric and rubber texture, cinematic lighting, aspect ratio 16:9`
  * **Runway (비디오)**: `Fast slow-motion of the running shoes striking the ground, heavy motion blur, highly dynamic movement forward`
* **결과 파일명**: `Nike_scene02_Gemini.png` / `Nike_scene02_Runway.mp4`

💡 **프롬프트 수정 및 개선 로그 (과제 필수 가점 포인트!)**
* **수정 전 의도**: Runway에서 Text-to-Video로 "나이키 신발을 신고 밤에 달리는 사람"을 바로 생성 시도.
* **문제점**: 무료 비디오 생성 AI 특성상 텍스트만 주면 나이키 로고가 심하게 찌그러지고 인물의 다리가 뒤틀리는 오류가 빈번히 발생하여 무료 크레딧이 낭비됨.
* **수정 후 변경**: 구글 Gemini로 정확한 나이키 로고와 발 클로즈업 정지 이미지를 완성도 높게 먼저 뽑은 후, Runway의 Image-to-Video 기능을 통해 '움직임만 추가'하는 파이프라인으로 전환.
* **결과 변화**: 고질적인 AI의 형태 왜곡 오류를 완벽하게 방지하면서, Runway 무료 크레딧 단 1회 만에 성공적인 결과물을 확보함.

### 🎬 씬 3 (Outro: 브랜드 정체성 및 슬로건 각인)
* **씬 번호 / 길이**: #3 / 3초
* **화면 구성**: 암전된 화면 중앙에 나이키 화이트 스우시 로고와 **JUST DO IT.** 슬로건 등장
* **내레이션/카피**: (화면 카피) "JUST DO IT."
* **사용 도구 및 목적**:
  * **시각 소스**: 통합 편집 툴 (CapCut / Premiere Pro 등) ➡️ Runway 무료 플랜 사용 시 발생하는 우측 하단 워터마크(Watermark)를 가리기 위해, 최종 편집 단계에서 화면 비율을 약간 조절(Crop)하거나 자막 레이어를 배치하는 현실적인 제약 극복 전략 적용.
  * **오디오 소스**: 유튜브 오디오 라이브러리 (Google) ➡️ 구글 생태계 내의 저작권 무료 음원 중 'Ambient Cinematic' 장르의 음악과 심장 박동 효과음(Heartbeat)을 다운로드하여 매칭.
* **결과 파일명**: `Nike_scene03_Logo.mp4` / `Nike_free_bgm.mp3`

---

## 3. 무료 플랜 제약 조건 극복 전략 설명 (최종 요약)

* **크레딧 절감 전략**: 무작위성이 심한 Text-to-Video 대신 고화질 이미지를 기반으로 비디오를 만드는 Image-to-Video 방식을 100% 채택하여 실패 확률과 크레딧 낭비를 제로에 가깝게 줄였습니다.
* **워터마크 및 해상도 대응**: Runway 무료 버전의 720p 제한 및 워터마크 노출 문제는 CapCut 등의 편집 프로그램에서 영상 스케일을 105%로 미세하게 확대 크롭하고, 자막 및 시네마틱 블랙 바(Letterbox)를 삽입하는 편집 기술적 가공을 통해 극복하도록 파이프라인을 설계했습니다.
