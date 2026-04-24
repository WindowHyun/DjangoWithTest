# 🧪 Pybo 서비스 전수 테스트 설계서 (Full-Inventory Spec v5.5)

## ✅ Part 1. 테스트 체크리스트 (전수 검사항목)

### 1.1. 인증 및 계정 (Auth & Profile)
- [ ] **회원가입**: 중복 아이디, 비밀번호 불일치, 이메일 형식 유효성 검증.
- [ ] **로그인/아웃**: 로그인 후 이전 페이지(`next`) 유지 및 세션 만료 처리.
- [ ] **계정 관리**: 비밀번호 재설정 메일 발송 및 토큰 유효성 검증.
- [ ] **프로필**: 사용자가 작성한 질문/답변/댓글 목록의 정확한 카운트 및 링크 연결.

### 1.2. 질문 및 카테고리 (Question & Category)
- [ ] **CRUD**: 제목(200자), 내용(필수) 제한 및 마크다운 렌더링 정확도.
- [ ] **카테고리**: 질문 생성 시 카테고리 지정 및 목록에서의 카테고리 필터링.
- [ ] **추천**: 본인 글 추천 금지 정책 및 중복 추천 방지 로직.

### 1.3. 답변 및 댓글 (Answer & Comment)
- [ ] **연동**: 질문에 귀속된 답변의 리스트업 및 답변에 귀속된 댓글의 계층적 노출.
- [ ] **권한**: 수정/삭제 버튼의 조건부 노출(작성자 전용) 및 서버측 권한 검증.
- [ ] **UI 피드백**: 등록/수정 후 앵커(`#`)를 이용한 정확한 위치 이동.

### 1.4. 검색, 정렬 및 페이징 (Search & Pagination)
- [ ] **검색**: 제목, 내용, 질문작성자, 답변작성자 4개 영역 통합 검색(`Q`객체).
- [ ] **정렬**: 추천순, 답변순, 최신순 집계(`Annotate`) 및 정렬 정합성.
- [ ] **페이징**: 페이지당 10개 게시물 노출 및 검색/정렬 파라미터 보존.

---

## 🧪 Part 2. 상세 테스트 케이스 (Detailed TCs - Total 55)

### 2.1. 유닛 테스트 (Unit Level - L1: Logic & Model)

| TC ID | 기능 | 테스트 목표 | 입력 데이터 (Variable: Type = Value) | 기대 결과 (Assertion) |
| :--- | :--- | :--- | :--- | :--- |
| **UT-01** | Markdown | # 헤더 변환 | `val: str = "# H1"` | `assert "<h1>H1</h1>" in result` |
| **UT-02** | Markdown | nl2br 개행 지원 | `val: str = "Line1\nLine2"` | `assert "<br />" in result` |
| **UT-03** | Model | Question __str__ | `subject: str = "Test Subject"` | `assert str(q) == "Test Subject"` |
| **UT-04** | Model | Question Voter count | `user: User` (voter.add) | `assert q.voter.count() == 1` |
| **UT-05** | Filter | 날짜 포맷팅 필터 | `date: datetime(2026, 4, 24)` | `assert "2026년 4월 24일" in result` |
| **UT-06** | Form | 제목 길이 제한 검증 | `subject: str = "A" * 201` | `assert form.is_valid() == False` |
| **UT-07** | Form | 이메일 형식 검증 | `email: str = "not-an-email"` | `assert "email" in form.errors` |
| **UT-08** | Model | Category Slug 생성 | `name: str = "자유게시판"` | `assert cat.slug == "자유게시판"` |
| **UT-09** | Util | 페이징 윈도우 계산 | `page: int = 12` | `assert range_start == 11` |
| **UT-10** | Auth | 비밀번호 유효성 | `pw: str = "123"` | `assert validate_password(pw)` raises Error |

### 2.2. 통합 테스트 (Integration Level - L2: View & DB)

| TC ID | 기능 | 테스트 목표 | 사전 조건 | 테스트 스텝 | 기대 결과 (Assertion) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **IT-11** | 검색 | 제목 검색 결과 | 질문 1개 존재 | `Question.objects.filter(subject__icontains="X")` | `assert count == 1` |
| **IT-12** | 검색 | 질문 내용 검색 | 질문 1개 존재 | `Question.objects.filter(content__icontains="Y")` | `assert count == 1` |
| **IT-13** | 검색 | 답변 작성자 검색 | 답변 1개 생성 | `Question.objects.filter(answer__author__username="Z")` | `assert exists == True` |
| **IT-14** | 검색 | 답변 내용 검색 | 답변 1개 생성 | `Question.objects.filter(answer__content__icontains="W")` | `assert exists == True` |
| **IT-15** | 정렬 | 추천순 정렬 쿼리 | 추천 3, 1, 5 | `order_by('-num_voter')` | `first.id == id_of_vote_5` |
| **IT-16** | 정렬 | 답변순 정렬 쿼리 | 답변 2, 0, 4 | `order_by('-num_answer')` | `first.id == id_of_answer_4` |
| **IT-17** | 권한 | 타인 글 수정 차단 | 타인 글 존재 | `client.post('/modify/id/')` | `response.status_code == 400` |
| **IT-18** | 삭제 | 질문 삭제 연쇄 | 질문1, 답변3 | `q.delete()` | `Answer.objects.count() == 0` |
| **IT-19** | 삭제 | 답변 삭제 연쇄 | 답변1, 댓글2 | `a.delete()` | `Comment.objects.count() == 0` |
| **IT-20** | 댓글 | 질문 댓글 정합성 | 질문 존재 | `Comment.objects.create(question=q)` | `c.question == q` |
| **IT-21** | 가입 | 중복 ID 가입 시도 | user1 존재 | `SignupForm(data={'username': 'user1'})` | `form.is_valid() == False` |
| **IT-22** | 로그인 | 로그인 Redirect | `next` 파라미터 | `client.post('/login/', data)` | `response.url == next_url` |
| **IT-23** | 프로필 | 활동 통계 정확성 | 글3 작성 | `Profile.objects.get()` | `questions_count == 3` |
| **IT-24** | 추천 | 중복 추천 차단 | 이미 추천함 | `q.voter.add(user)` | `voter.count()` 변함없음 |
| **IT-25** | 페이징 | 마지막 페이지 조회 | 25개 존재 | `Paginator(objs, 10).page(3)` | `len(object_list) == 5` |
| **IT-26** | 카테고리 | 카테고리 필터링 | '질문' 카테고리 | `Question.objects.filter(category__name='질문')` | 해당 카테고리 글만 추출 확인 |
| **IT-27** | 비밀번호 | 초기화 토큰 생성 | 유저 존재 | `default_token_generator.make_token(user)` | 유효한 토큰 문자열 반환 확인 |
| **IT-28** | 보안 | CSRF 토큰 검증 | POST 요청 | `client.post('/create/', data)` | CSRF 미포함 시 403 반환 확인 |
| **IT-29** | 모델 | Modify Date 갱신 | 질문 수정 | `q.save()` after modify | `modify_date`가 생성일보다 큼 확인 |
| **IT-30** | 뷰 | 비로그인 글쓰기 차단 | 비로그인 | `GET /pybo/question/create/` | `response.status_code == 302` (Login) |

### 2.3. UI / E2E 테스트 (UI Level - L3: Browser & Scenario)

| TC ID | 기능 | 테스트 목표 | 사전 조건 | 테스트 스텝 | 기대 결과 (Assertion) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **UI-31** | BVT | 질문 등록 및 확인 | 로그인 | 1.글쓰기 2.내용입력 3.저장 | 목록 최상단에 제목 노출 확인 |
| **UI-32** | 질문 | 질문 수정 동작 | 본인 글 | 1.수정 2.내용변경 3.저장 | 상세페이지 변경내용 반영 확인 |
| **UI-33** | 질문 | 질문 삭제 동작 | 본인 글 | 1.삭제 2.컨펌 확인 | 목록페이지로 이동 및 글 삭제 확인 |
| **UI-34** | 답변 | 답변 등록 및 앵커 | 질문 상세 | 1.답변입력 2.등록 | URL#answer_ID 포함 및 스크롤 이동 |
| **UI-35** | 답변 | 답변 수정 및 앵커 | 본인 답변 | 1.수정 2.저장 | 수정내용 반영 및 앵커 유지 확인 |
| **UI-36** | 답변 | 답변 삭제 | 본인 답변 | 1.삭제 2.컨펌 | 해당 답변 요소 DOM에서 제거 확인 |
| **UI-37** | 댓글 | 질문 댓글 추가 | 질문 상세 | 1.댓글버튼 2.입력 3.저장 | 질문 하단 댓글 리스트 즉시 반영 |
| **UI-38** | 댓글 | 답변 댓글 추가 | 답변 영역 | 1.댓글버튼 2.입력 3.저장 | 답변 하단 댓글 리스트 즉시 반영 |
| **UI-39** | 추천 | 질문 추천 실시간 | 상세 | 1.추천클릭 | 추천수 카운트 1 증가 확인 |
| **UI-40** | 추천 | 본인 글 추천 차단 | 본인 상세 | 1.추천클릭 | "본인 글은 추천 불가" 얼럿 노출 |
| **UI-41** | 검색 | 제목 검색 결과 | 목록 | 1.검색어입력 2.엔터 | 결과 목록에 검색어 포함 확인 |
| **UI-42** | 정렬 | 추천순 정렬 UI | 목록 | 1.정렬:추천순 선택 | 첫 게시물 추천수 최대값 확인 |
| **UI-43** | 페이징 | 페이지 클릭 이동 | 20개 게시물 | 1. 2페이지 번호 클릭 | URL 파라미터 `page=2` 포함 확인 |
| **UI-44** | 복합 | 검색 후 페이징 유지 | 검색 결과 | 1. 2페이지 클릭 | URL에 `kw`와 `page` 파라미터 공존 |
| **UI-45** | 복합 | 정렬 후 페이징 유지 | 정렬 결과 | 1. 2페이지 클릭 | URL에 `so`와 `page` 파라미터 공존 |
| **UI-46** | 가입 | 필수값 누락 가입 | 가입 화면 | 1.ID만 입력 2.가입 | 에러 메시지(`alert-danger`) 노출 |
| **UI-47** | 가입 | PW 불일치 검증 | 가입 화면 | 1.다른 PW 2개 입력 2.가입 | "비밀번호가 일치하지 않습니다" 노출 |
| **UI-48** | 로그인 | 오정보 로그인 시도 | 로그인 화면 | 1.틀린정보입력 2.로그인 | "아이디/비번을 확인하세요" 노출 |
| **UI-49** | 권한 | 수정버튼 은닉 확인 | 타인 글 | 1.상세페이지 접속 | `.btn-modify` 요소가 보이지 않음 |
| **UI-50** | 프로필 | 활동 링크 동작 | 프로필 | 1.작성 질문 제목 클릭 | 해당 질문 상세로 정상 이동 확인 |
| **UI-51** | 보안 | 마크다운 XSS 차단 | 글쓰기 | 1.<script>alert(1)</script> 입력 <br> 2.저장 버튼 클릭 <br> 3.상세 페이지 확인 | `content: str = "<script>alert(1)</script>"` | 브라우저 알럿이 실행되지 않아야 하며, 태그가 텍스트로 노출되거나 필터링됨 확인 | 글 삭제 |
| **UI-52** | 반응형 | 모바일 메뉴 토글 동작 | 메인 페이지 (375px) | 1.브라우저 너비를 375px로 조정 <br> 2.우측 상단 햄버거 메뉴 아이콘 클릭 | `Viewport: 375x667` <br> `Locator: .navbar-toggler` | 네비게이션 메뉴 리스트(로그인, 가입 등)가 아래로 펼쳐지며 노출 확인 | - |
| **UI-53** | 앵커 | 외부 링크 직접 접속 시 앵커 이동 | 브라우저 주소창 | 1.특정 답변의 앵커가 포함된 URL 입력 및 이동 <br> (`/pybo/1/#answer_5`) | `URL: str = "/pybo/1/#answer_5"` | 페이지 로드 후 즉시 해당 답변 위치(`#answer_5`)로 스크롤 이동 확인 | - |
| **UI-54** | 초기화 | 비밀번호 찾기 메일 안내 | 비번 찾기 페이지 | 1.등록된 이메일 주소 입력 <br> 2.비밀번호 재설정 버튼 클릭 | `email: str = "test@example.com"` <br> `Locator: button[type=submit]` | "비밀번호 재설정 안내 메일을 발송했습니다" 메시지(`alert-info`) 노출 확인 | - |
| **UI-55** | 레이아웃 | 질문 상세 작성자 정보 노출 | 질문 상세 페이지 | 1.로그인 후 질문 상세 페이지 접속 <br> 2.우측 하단 작성자 정보 영역 확인 | `Locator: .badge.bg-light` | 작성자의 아이디와 작성 일시가 명확하게 노출되는지 확인 | - |

