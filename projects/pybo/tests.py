from django.test import TestCase
from django.utils import timezone

from .models import *


# Create your tests here.
class PyboIndexTest(TestCase):
#TC-1. 경로 요청 시 200 상태 코드를 변환하는지 테스트
#TC-2. 경로 진입 후 특정 텍스트가 포함되어 있는지 확인

    def test_index_status(self):
        response = self.client.get('/pybo/')
        self.assertEqual(response.status_code, 200)

    def test_index_content(self):
        response = self.client.get('/pybo/')
        self.assertContains(response, "질문이 없습니다.")

class QuestionModelTest(TestCase):
    # TC-1. 테스트 데이터 생성
    def test_question_create(self):
        q = Question.objects.create(
            subject="첫 번째 질문입니다.",
            content ="테스트 데이터 생성중입니다.",
            create_date=timezone.now()
        )

    # TC-2. 데이터가 DB에 잘 입력되었는지 확인
        self.assertEqual(q.subject, "첫 번째 질문입니다.")
        self.assertEqual(Question.objects.count(), 1)

    def test_answer_create(self):

        #TC-1. 질문 목데이터 생성하기
        q = Question.objects.create(
            subject="첫 번째 질문입니다.",
            content ="테스트 데이터 생성중입니다.",
            create_date=timezone.now()
        )


        #TC-2 q 인스턴스 전달받아 answer 데이터 생성
        a = Answer.objects.create(
            question = q,
            content = "테스트 답변중입니다.",
            create_date=timezone.now()
        )

        #TC-3 content 데이터가 '테스트'로 시작하는지 확인 
        self.assertTrue(a.content.startswith("테스트")) ## 테스트로 시작
        self.assertEqual(Answer.objects.count(), 1)

class PyboViewTest(TestCase):
    def setUp(self):
            # 테스트 진행 전 데이터 생성
        Question.objects.create(
            subject="테스트 질문입니다.",
            content ="테스트 데이터 생성중입니다.",
            create_date=timezone.now()
        )

    def test_index_view_with_questions(self):
        # index 페이지 진입 후 DB에 질문이 정상적으로 노출되는지 테스트

        response = self.client.get('/pybo/')
            
        # TC-1 : 응답 상태 200 확인
        self.assertEqual(response.status_code,200)
            
        # TC-2 : 응답 내용에 setUp 에서 만들어진 질문 제목이 포함 되어있는지 확인
        self.assertContains(response, "테스트")

        # TC-3 : 템플릿에 전달된 question_list에 데이터가 있는지 확인
        self.assertEqual(len(response.context['question_list']),1)


class PyboDetailViewTest(TestCase):

    def setUp(self):
            # 테스트 진행 전 데이터 생성
        self.question = Question.objects.create(
            subject="테스트 질문입니다.",
            content ="테스트 데이터 생성중입니다.",
            create_date=timezone.now()
        )

    def test_detail_view_status(self):
        response = self.client.get(f'/pybo/{self.question.id}/')
        self.assertEqual(response.status_code,200)

    def test_detail_view_content(self):
        response = self.client.get(f'/pybo/{self.question.id}/')
        self.assertContains(response, self.question.subject)
        self.assertContains(response, self.question.content)

    def test_detail_view_context(self):
        response = self.client.get(f'/pybo/{self.question.id}/')
        self.assertEqual(response.context['question'], self.question)


class PyboDetailObjector404(TestCase):
    def setUp(self):
            # 테스트 진행 전 데이터 생성
        self.question = Question.objects.create(
            subject="테스트 질문입니다.",
            content ="테스트 데이터 생성중입니다.",
            create_date=timezone.now()
        )

    def test_detail_view_success(self):
        response = self.client.get(f'/pybo/{self.question.id}/')
        self.assertEqual(response.status_code,200)

        self.assertContains(response, self.question.subject)
        self.assertEqual(response.context['question'], self.question)

    def test_detail_view_404(self):
        response = self.client.get('/pybo/999/')
        self.assertEqual(response.status_code,404)