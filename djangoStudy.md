## uv 설치

1. powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
2. uv --version

### 프로젝트 생성하기

> 루트 디렉터리 접근
1. uv init mysite --python 3.14
2. uv add django
3. uv run django-admin startproject config .

> 개발 서버 구동
1. uv run manage.py runserver

> 한국어 세팅
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'

## startapp 

>migrations : 파일이 아닌 디렉터리이며, 장고가 데이터베이스 테이블을 생성하고 수정하기 위한 파일들을 이곳에서 관리한다.
admin.py : 장고 관리자 화면을 구성하는 파일이다. 이곳에 코드를 추가하여 관리자 화면을 제어할 수 있다.
apps.py : 앱의 구성 정보를 정의하는 파일이다. (파이보 프로젝트에서 이 파일을 수정할 일은 없다.)
models.py : 데이터베이스 모델을 정의하는 파일이다.
tests.py : 앱을 테스트할 때 사용하는 파일이다.
views.py : 앱의 기능을 구현하는 파일이다. 앞으로 가장 많이 사용할 파일이다.
