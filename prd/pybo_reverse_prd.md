# 📄 [역기획서] Pybo 커뮤니티 게시판 - v5.1 (Full Spec with API Inventory)

## 1. 프로젝트 정의 및 용어 (Definitions & Glossary)
- **Pybo**: Python과 Board의 합성어로, 본 프로젝트의 서비스 명칭.
- **질문(Question)**: 사용자가 게시하는 주 게시물.
- **답변(Answer)**: 질문에 대해 사용자가 등록하는 해결책.
- **추천(Vote)**: 게시물의 유용성을 평가하는 지표 (추천인 수 기반).
- **앵커(Anchor)**: 특정 답변이나 댓글로 즉시 스크롤 시키기 위한 고유 식별자(ID).

## 2. 데이터 모델 명세 (Data Schema)
| Model | Field | Type | Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Question** | `subject` | CharField | Max: 200, Not Null | 질문 제목 |
| | `content` | TextField | Not Null | 마크다운 지원 내용 |
| | `author` | ForeignKey | User, Protect | 작성자 (탈퇴 시 게시물 보호) |
| | `voter` | ManyToMany | User | 추천인 목록 |
| **Answer** | `question` | ForeignKey | Question, Cascade | 소속 질문 (질문 삭제 시 삭제) |
| | `content` | TextField | Not Null | 답변 내용 |

## 3. 전수 API 및 엔드포인트 명세 (API Inventory)

### 3.1. 질문(Question) 서비스
| Method | Path | 파라미터 | 목적 및 리다이렉션 |
| :--- | :--- | :--- | :--- |
| `GET` | `/pybo/` | `page`, `kw`, `so` | 질문 목록 조회 (index) |
| `GET` | `/pybo/<int:q_id>/` | - | 질문 상세 및 답변 목록 조회 (detail) |
| `GET/POST`| `/pybo/question/create/` | `subject`, `content` | 질문 작성 및 저장 -> `/pybo/` |
| `GET/POST`| `/pybo/question/modify/<int:q_id>/`| `subject`, `content` | 질문 수정 및 저장 -> 상세 페이지 |
| `GET` | `/pybo/question/delete/<int:q_id>/`| - | 질문 삭제 -> `/pybo/` |
| `GET` | `/pybo/question/vote/<int:q_id>/` | - | 질문 추천 처리 -> 상세 페이지 |

### 3.2. 답변(Answer) 서비스
| Method | Path | 파라미터 | 목적 및 리다이렉션 |
| :--- | :--- | :--- | :--- |
| `POST` | `/pybo/answer/create/<int:q_id>/` | `content` | 답변 등록 -> 상세 페이지 (Anchor 이동) |
| `GET/POST`| `/pybo/answer/modify/<int:a_id>/` | `content` | 답변 수정 -> 상세 페이지 (Anchor 이동) |
| `GET` | `/pybo/answer/delete/<int:a_id>/` | - | 답변 삭제 -> 상세 페이지 |
| `GET` | `/pybo/answer/vote/<int:a_id>/` | - | 답변 추천 처리 -> 상세 페이지 |

### 3.3. 공통/인증(Common/Auth) 서비스
| Method | Path | 파라미터 | 목적 |
| :--- | :--- | :--- | :--- |
| `GET/POST`| `/common/login/` | `username`, `password` | 로그인 (next 파라미터 지원) |
| `GET` | `/common/logout/` | - | 로그아웃 처리 |
| `GET/POST`| `/common/signup/` | `username`, `password`, `email` | 신규 회원가입 |

## 4. 상세 비즈니스 정책 (Deep Business Rules)
- **검색(Search)**: `Q` 객체를 사용하여 제목/내용/작성자/답변작성자 4개 필드 통합 검색.
- **정렬(Sorting)**: `Annotate`를 활용하여 추천수/답변수 카운트 기준 동적 정렬.
- **보안**: CSRF Token 필수 및 서버사이드 작성자 권한 검증(`if request.user != author`).

## 5. UI/UX 상세 로직 (Layout & Interaction)
- **페이징(Pagination)**: 검색어(`kw`)와 정렬(`so`) 파라미터가 유지된 상태로 페이지 이동 처리.
- **앵커 시스템**: 답변 수정/등록 시 `redirect` URL 뒤에 `#answer_<id>`를 붙여 해당 위치로 자동 포커싱.

## 6. 수락 조건 (Acceptance Criteria)
1. [ ] 비로그인 사용자가 추천 클릭 시 로그인 페이지로 이동하고, 로그인 후 원래 상세 페이지로 복귀하는가?
2. [ ] 질문 검색 시 답변을 단 사람의 이름으로도 결과가 정상 노출되는가?
3. [ ] 답변 등록 시 페이지가 새로고침된 후, 내가 쓴 답변 위치로 자동 스크롤(Anchor) 되는가?
4. [ ] 본인이 작성하지 않은 글의 수정/삭제 버튼이 UI상에서 보이지 않으며, URL 강제 진입 시 400 에러를 반환하는가?

## 7. 비기능적 요구사항 (Non-Functional)
- **성능**: 대량 데이터 상황에서도 페이징 처리가 200ms 이내에 완료될 것.
- **보안**: 마크다운 렌더링 시 악의적인 스크립트 실행이 차단될 것.

---
**[수석 QA 분석가 최종 의견]**
이제 기획서에 모든 API 엔드포인트와 파라미터 정보가 포함되었습니다. 특히 `/pybo/` 목록 API의 `kw`, `so` 파라미터가 페이징과 결합될 때의 동작을 검증하는 것이 이번 프로젝트 테스트의 핵심입니다.
