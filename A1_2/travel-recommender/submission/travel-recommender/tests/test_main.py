import contextlib
import io
import json
import os
import socket
import tempfile
import types
import unittest
from urllib.error import URLError
from pathlib import Path
from unittest.mock import patch

import main


RECOMMENDATION = {
    "recommended_city": "강릉", "weather": "선선한 가을 날씨",
    "events": ["지역 축제 후보 (개최 확인 필요)"],
    "reason": "바다를 산책하기 좋습니다. 가을 풍경을 즐길 수 있습니다.",
}
PLACE = {"title": "<b>테스트</b> 식당", "address": "강릉시 테스트로 1",
         "roadAddress": "", "category": "음식점", "link": "https://example.com/place",
         "mapx": "1289000000", "mapy": "377000000"}


class TravelTests(unittest.TestCase):
    def test_dns_failure_has_specific_message(self):
        with patch.object(main, "urlopen", side_effect=URLError(socket.gaierror(8, "DNS failed"))):
            with self.assertRaisesRegex(main.APIError, "DNS 조회 실패"):
                main.request_json("https://example.com", {})

    def test_invalid_dates_and_missing_argument(self):
        for args in ([], ["-date", "2026-02-30"], ["-date", "2026-1-01"], ["-date", "oops"]):
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
                main.main(args)
            self.assertEqual(raised.exception.code, 2)
        self.assertEqual(main.parse_date("2028-02-29"), "2028-02-29")

    def run_flow(self, responses, expected_code=0, keys=True):
        env = {"CODYSSEY_API_KEY": "test-codyssey", "NAVER_CLIENT_ID": "test-naver-id", "NAVER_CLIENT_SECRET": "test-naver-secret"} if keys else {}
        fake_dotenv = types.SimpleNamespace(load_dotenv=lambda *a, **k: None)
        with tempfile.TemporaryDirectory() as folder:
            with patch.dict(os.environ, env, clear=True), patch.dict("sys.modules", {"dotenv": fake_dotenv}), \
                    patch.object(main, "BASE_DIR", Path(folder)), \
                    patch.object(main, "request_json", side_effect=responses) as request, \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main.main(["-date", "2026-11-14"]), expected_code)
            if not keys:
                request.assert_not_called()
                self.assertFalse((Path(folder) / "results").exists())
                return
            files = list((Path(folder) / "results").glob("*.json"))
            self.assertEqual(len(files), 1)
            data = json.loads(files[0].read_text(encoding="utf-8"))
            report = files[0].with_suffix(".md").read_text(encoding="utf-8")
            self.assertIn("## errors", report)
            self.assertNotIn("test-codyssey", report + json.dumps(data))
            self.assertNotIn("test-naver-secret", report + json.dumps(data))
            return data, report, request.call_args_list

    def test_full_pipeline_and_coordinates(self):
        data, report, calls = self.run_flow([
            completion(json.dumps(RECOMMENDATION)), {"items": [PLACE]}, completion("오전: 산책, 오후: 관람, 저녁: 식사")])
        self.assertEqual(data["restaurants"][0]["x"], 1289000000)
        self.assertEqual(data["errors"], [])
        self.assertEqual(calls[0].args[0], "https://copa.codyssey.kr/v1/chat/completions")
        self.assertEqual(calls[0].args[1]["Authorization"], "Bearer test-codyssey")
        self.assertEqual(calls[0].args[2]["model"], "gpt-5-mini")
        self.assertNotIn("response_format", calls[0].args[2])
        self.assertIn("테스트 식당", report)
        self.assertEqual(calls[1].args[1]["X-NCP-APIGW-API-KEY-ID"], "test-naver-id")
        self.assertEqual(calls[1].args[1]["X-NCP-APIGW-API-KEY"], "test-naver-secret")
        self.assertIn("https://naverapihub.apigw.ntruss.com/search/v1/local?", calls[1].args[0])
        self.assertIn("format=json", calls[1].args[0])
        self.assertIn("%EA%B0%95%EB%A6%89", calls[1].args[0])
        self.assertIn("테스트 식당", calls[2].args[2]["messages"][1]["content"])

    def test_empty_and_failed_map(self):
        for response in ({"items": []}, main.APIError("HTTP 403: 권한 확인"), {"items": None}):
            with self.subTest(response=response):
                data, report, _ = self.run_flow([
                    completion(json.dumps(RECOMMENDATION)), response, completion("여행 제안")])
                self.assertEqual(data["restaurants"], [])
                self.assertIn("데이터 없음", report)
                self.assertEqual(bool(data["errors"]), response != {"items": []})

    def test_json_retry_and_final_fallback(self):
        data, report, calls = self.run_flow([
            completion('{"events": "wrong type"}'), completion(json.dumps(RECOMMENDATION)),
            {"items": []}, main.APIError("네트워크 연결 실패")])
        self.assertEqual(len(data["errors"]), 2)
        self.assertIn("## 1일 일정 제안", report)
        self.assertEqual(len(calls), 4)

    def test_unparseable_json_and_missing_keys(self):
        data, _, calls = self.run_flow([completion("not JSON"), completion("not JSON")], expected_code=1)
        self.assertIsNone(data["recommendation"])
        self.assertEqual(len(calls), 2)
        self.run_flow([], expected_code=1, keys=False)


def completion(text):
    return {"choices": [{"message": {"content": text}}]}


if __name__ == "__main__":
    unittest.main()
