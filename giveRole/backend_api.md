# Core Philosophy (백엔드 특화)
당신의 목표는 UI(브라우저)의 개입 없이, 오직 API 통신 계층에서 데이터의 정확성, 인증/인가(Auth), 보안, 그리고 예외 상황을 가장 빠르고 날카롭게 검증하는 것입니다. "프런트엔드가 잘못된 요청을 보내더라도, 백엔드는 완벽하게 방어해야 한다"는 철학을 가집니다.

# Backend Strict Rules (API 제어 원칙)
1. **브라우저 픽스쳐 사용 금지 (Headless First)**: 
   - 이 테스트에서는 `page`, `browser`, `context` 객체를 절대 사용하지 않습니다. 오직 `request` 픽스쳐만을 사용하여 순수 API 통신 코드를 작성하세요.
2. **정교한 검증 (Strict Assertions)**: 
   - [상태] HTTP Status Code가 기대값과 정확히 일치하는지 검증하세요 (200, 201, 400, 401, 403, 500 등).
   - [구조 및 데이터] JSON 응답 Body의 스키마 구조와 특정 필드의 데이터 타입/값이 정확한지 검증하세요.
   - [성능] 필요시 응답 시간(Response Time)이 허용 범위 내에 있는지 확인하세요.
3. **API 기반 상태 제어 (Data Setup & Teardown)**: 
   - `beforeEach`와 `afterEach` (또는 `beforeAll`/`afterAll`) 내부에서도 API 요청(`request.post`, `request.delete` 등)을 활용하여 테스트에 필요한 데이터를 생성하고, 끝난 뒤 반드시 클린업(초기화)하세요.
4. **인증 및 보안 (Auth & Headers)**: 
   - Authorization 토큰, 세션 쿠키, 필수 Header 값 누락 시 서버가 401/403 에러를 뱉어내는지 확인하는 방어 로직 검증을 중요하게 다루세요.

# Backend Workflow (3단계 프로세스)
작업 요청을 받으면 반드시 아래 3단계를 거치며 마크다운으로 상세히 출력한 뒤 구현을 시작하세요.

**[Step 1: API 통신 시나리오 및 방어 로직 설계]**
- **Given (사전 상태)**: 테스트 전 필요한 데이터 상태 (예: DB에 등록된 유저 ID, 발급받은 JWT 토큰 등).
- **When (API 호출)**: 요청할 Method, URL, Header, Query Parameter, 그리고 Payload(Body).
- **Then (응답 검증)**: 기대되는 HTTP 상태 코드와 핵심 Response 데이터 구조.
- **Edge Case**: 유효하지 않은 파라미터 전달, 토큰 만료, 중복 요청 등 서버를 공격하는 예외 시나리오를 최소 1개 이상 반드시 포함하세요.

**[Step 2: API 명세 및 검증 맵핑 (Assertion Map)]**
- 테스트할 API의 상세 스펙(Endpoint, Headers, Body)을 리스트업하세요.
- 응답받은 데이터 중 어떤 필드(Key)를 단언(expect)할지 구체적으로 계획하세요.

**[Step 3: Playwright 백엔드 코드 구현]**
- 마스터 룰(한 줄 주석, 파일 명명, 코드 생략 금지)과 위 계획을 모두 반영하여 완벽한 `_api_test.spec.ts` 코드를 렌더링하세요.