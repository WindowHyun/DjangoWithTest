from django.test import TestCase


# Create your tests here.
class PyboIndexTest(TestCase):
#TC-1. 경로 요청 시 200 상태 코드를 변환하는지 테스트
#TC-2. 경로 진입 후 특정 텍스트가 포함되어 있는지 확인

    def test_index_status(self):
        response = self.client.get('/pybo/')
        self.assertEqual(response.status_code, 200)

    def test_index_content(self):
        response = self.client.get('/pybo/')
        self.assertContains(response, "안녕하세요 pybo에 오신것을 환영합니다.")