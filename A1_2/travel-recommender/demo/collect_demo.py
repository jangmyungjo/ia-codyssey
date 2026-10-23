import json
import subprocess
import textwrap
from pathlib import Path
root = Path(__file__).resolve().parent.parent
pages = []
def add(title, text):
    lines = []
    for line in text.splitlines():
        lines.extend(textwrap.wrap(line, width=64, replace_whitespace=False) or [''])
    for offset in range(0, len(lines), 18):
        pages.append({'title': title, 'text': '\n'.join(lines[offset:offset+18])})
add('국내 여행 추천 CLI · 실행 검증', '실제 실행 로그와 결과 파일을 영상으로 변환했습니다.\n화면을 직접 촬영한 녹화 영상은 아닙니다.\n\nLLM: Codyssey / gpt-5-mini\n장소 검색: NAVER API HUB\n여행 날짜: 2026-11-14\n인증 정보는 영상에 포함하지 않습니다.')
for title, args in [('날짜 검증', ['main.py', '-date', '2026-02-30']), ('자동 테스트', ['-m', 'unittest', 'discover', '-s', 'tests', '-v']), ('실제 API 실행', ['-u', 'main.py', '-date', '2026-11-14'])]:
    print(title, '진행 중', flush=True)
    result = subprocess.run([str(root/'.venv/bin/python'), *args], cwd=root, text=True, capture_output=True, timeout=210)
    output = result.stdout + result.stderr
    add(title, '$ python ' + ' '.join(args) + '\n\n' + output + '\n종료 코드: ' + str(result.returncode))
    if title == '실제 API 실행':
        if result.returncode:
            raise SystemExit('실제 API 실행 실패: 영상을 성공 사례로 만들지 않습니다.')
        paths = [line.removeprefix('저장 완료: ') for line in output.splitlines() if line.startswith('저장 완료: ') and line.endswith('.md')]
        report = Path(paths[-1])
        add('생성된 여행 리포트', report.read_text())
        add('검증 완료', 'CLI 실행 성공\n맛집 검색과 LLM 리포트 생성 완료\n\n결과 파일:\n' + report.name + '\n' + report.with_suffix('.json').name)
(root/'demo/pages.json').write_text(json.dumps(pages, ensure_ascii=False))
(root/'demo/run_log.txt').write_text('\n\n'.join(p['title']+'\n'+p['text'] for p in pages))
print('실제 실행 자료 수집 완료:', len(pages), '페이지', flush=True)
