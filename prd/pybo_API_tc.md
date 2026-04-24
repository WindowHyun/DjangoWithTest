# 🧪 Pybo 서비스 전수 API 테스트 설계서 (API-Level Spec v1.1 - Final 4-17 Base)

## 1. API 테스트 체크리스트
- [ ] **네임스페이스**: 모든 리다이렉트가 `pybo:` 및 `common:` 네임스페이스 규칙을 준수하는가?
- [ ] **HTTP 상태 코드**: 
  - 성공(GET): 200
  - 성공(POST): 302 (Redirect)
  - 권한/로직 위반: 302 (Error Message 포함하여 Redirect) 또는 400
- [ ] **댓글 데이터 정합성**: 댓글 생성 시 `question_id` 또는 `answer_id` 중 하나만 세팅되고 나머지는 Null인지 확인.
- [ ] **인증 리다이렉트**: `@login_required`에 의해 비인증 유저가 `/common/login/?next=...`로 정확히 이동하는가?

---

## 2. 상세 API 테스트 케이스 (Detailed API TCs)

### 2.1. 질문(Question) API
| TC ID | 기능 | Method | Path | Request Data (Variable: Type = Value) | Expected Status | Assertion (Expected Result) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **API-01** | 목록 조회 | `GET` | `/pybo/` | `kw: str`, `page: int`, `so: str` | 200 | `question_list` 객체 및 페이징 정보 포함 |
| **API-02** | 상세 조회 | `GET` | `/pybo/<int:q_id>/` | - | 200 | 질문/답변/댓글 트리 구조 데이터 로드 확인 |
| **API-03** | 질문 생성 | `POST` | `/pybo/question/create/` | `subject: str`, `content: str` | 302 | `redirect('pybo:index')` 확인 및 DB 생성 |
| **API-04** | 질문 수정 | `POST` | `/pybo/question/modify/<int:q_id>/` | `subject: str`, `content: str` | 302 | `redirect('pybo:detail', question_id=q_id)` 확인 |
| **API-05** | 질문 삭제 | `GET` | `/pybo/question/delete/<int:q_id>/` | - | 302 | `redirect('pybo:index')` 및 DB 삭제 확인 |
| **API-06** | 질문 추천 | `GET` | `/pybo/question/vote/<int:q_id>/` | - | 302 | `voter.add(user)` 후 상세 페이지 리다이렉트 |
| **API-07** | 타인 글 수정 차단 | `POST` | `/pybo/question/modify/<int:q_id>/` | 타인 글 ID | 302 | `messages.error` 발생 및 상세 페이지로 리다이렉트 |

### 2.2. 답변(Answer) API
| TC ID | 기능 | Method | Path | Request Data (Variable: Type = Value) | Expected Status | Assertion (Expected Result) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **API-08** | 답변 등록 | `POST` | `/pybo/answer/create/<int:q_id>/` | `content: str` | 302 | `redirect('...#answer_ID')` 앵커 포함 확인 |
| **API-09** | 답변 수정 | `POST` | `/pybo/answer/modify/<int:a_id>/` | `content: str` | 302 | `redirect('...#answer_ID')` 확인 |
| **API-10** | 답변 삭제 | `GET` | `/pybo/answer/delete/<int:a_id>/` | - | 302 | 상세 페이지 리다이렉트 및 DB 삭제 |
| **API-11** | 답변 추천 | `GET` | `/pybo/answer/vote/<int:a_id>/` | - | 302 | 추천수 증가 후 상세 페이지 리다이렉트 |

### 2.3. 댓글(Comment) API
| TC ID | 기능 | Method | Path | Request Data (Variable: Type = Value) | Expected Status | Assertion (Expected Result) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **API-12** | 질문 댓글 등록 | `POST` | `/pybo/comment/create/question/<int:q_id>/` | `content: str` | 302 | `Comment.question` 필드 할당 및 앵커 리다이렉트 |
| **API-13** | 답변 댓글 등록 | `POST` | `/pybo/comment/create/answer/<int:a_id>/` | `content: str` | 302 | `Comment.answer` 필드 할당 및 앵커 리다이렉트 |
| **API-14** | 댓글 수정 | `POST` | `/pybo/comment/modify/<int:c_id>/` | `content: str` | 302 | 상세 페이지 리다이렉트 및 내용 반영 확인 |
| **API-15** | 댓글 삭제 | `GET` | `/pybo/comment/delete/<int:c_id>/` | - | 302 | DB 삭제 및 상세 페이지 리다이렉트 |

### 2.4. 인증(Auth) API
| TC ID | 기능 | Method | Path | Request Data (Variable: Type = Value) | Expected Status | Assertion (Expected Result) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **API-16** | 회원가입 | `POST` | `/common/signup/` | `username`, `password`, `email` | 302 | 가입 후 메인 페이지 리다이렉트 |
| **API-17** | 로그인 | `POST` | `/common/login/` | `username`, `password` | 302 | 세션 생성 및 `next` 경로 이동 |
| **API-18** | 비밀번호 재설정 | `POST` | `/common/password_reset/` | `email: str` | 302 | 재설정 안내 메일 발송 큐 등록 확인 |

---

**[수석 QA 자동화 엔지니어 코멘트]**
- **4-17 전용 로직**: 댓글(`Comment`)이 질문과 답변에 공용으로 쓰이는 구조를 `API-12`, `IT-13`에서 명확히 검증하도록 설계했습니다.
- **Redirect 전략**: 모든 `POST` 요청에 대해 302 상태 코드와 함께, `Anchor(#)`가 포함된 상세 페이지로의 정확한 회귀를 검증하는 것이 자동화의 핵심입니다.
