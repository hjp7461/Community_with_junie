# 프로젝트 가이드라인

## 프로젝트 개요
이 프로젝트는 Django 기반 웹 애플리케이션입니다. 프로젝트는 표준 Django 프로젝트 구조와 규칙을 따릅니다.

## 디렉토리 구조
- `config/`: Django 프로젝트 설정 파일 포함
  - `settings/`: 다양한 환경에 대한 설정 포함
    - `base.py`: 모든 환경에서 공유되는 기본 설정
    - `development.py`: 개발 환경에 특화된 설정
    - `production.py`: 프로덕션 환경에 특화된 설정
  - `urls.py`: URL 라우팅 설정
  - `wsgi.py` 및 `asgi.py`: 웹 서버 게이트웨이 인터페이스
- `docs/`: 문서 파일
  - `requirements.md`: 프로젝트 요구사항 문서
- `static/`: 정적 파일 (CSS, JavaScript, 이미지 등)
- `templates/`: HTML 템플릿
  - `base.html`: 기본 템플릿 레이아웃
  - `home.html`: 홈페이지 템플릿
  - `users/`: 사용자 관련 템플릿
    - 로그인, 회원가입, 프로필 등의 템플릿
- `users/`: 사용자 관리 Django 앱
  - `models.py`: 사용자 모델 정의
  - `views.py`: 사용자 관련 뷰 함수
  - `forms.py`: 사용자 관련 폼
  - `urls.py`: 사용자 관련 URL 라우팅
  - `admin.py`: 관리자 인터페이스 설정
  - `signals.py`: 사용자 관련 시그널 처리
  - `migrations/`: 데이터베이스 마이그레이션 파일
- `.junie/`: 프로젝트 가이드라인 및 문서
  - `guidelines.md`: 프로젝트 가이드라인 문서

### 주요 파일
- `manage.py`: Django 프로젝트 관리 스크립트
- `db.sqlite3`: SQLite 데이터베이스 파일
- `pyproject.toml`: 프로젝트 의존성 및 설정
- `uv.lock`: 의존성 잠금 파일

## 개발 가이드라인

### 환경 설정
1. `.venv`를 사용하여 가상 환경 생성
2. 이 프로젝트는 Python 패키지 매니저 `uv`를 사용합니다. 패키지 설치 시 `uv` 또는 `uv pip` 명령어를 사용해야 합니다.
   ```
   # 패키지 설치 예시
   uv pip install -r requirements.txt
   # 또는
   uv install -r requirements.txt
   ```
3. `python manage.py migrate`로 마이그레이션 실행
4. `python manage.py runserver`로 개발 서버 시작

### 코딩 표준
- Python 코드에 대해 PEP 8 스타일 가이드 준수
- 의미 있는 변수 및 함수 이름 사용
- 모든 함수, 클래스 및 모듈에 대한 문서 문자열 작성
- 함수는 작게 유지하고 단일 작업에 집중

### Git 워크플로우
1. 각 기능 또는 버그 수정을 위한 새 브랜치 생성
2. 명확한 메시지가 있는 작고 집중된 커밋 작성
3. 메인 브랜치에 병합하기 전에 코드 리뷰를 위한 풀 리퀘스트 제출
4. 브랜치를 메인 브랜치와 최신 상태로 유지

### 테스팅
- 모든 새로운 기능 및 버그 수정에 대한 테스트 작성
- 풀 리퀘스트를 제출하기 전에 테스트 실행
- 높은 테스트 커버리지 목표

## 배포
- 프로젝트는 개발 및 프로덕션 환경에 대한 별도의 설정이 있음
- 프로덕션 서버에 배포할 때 프로덕션 설정 사용
- 모든 민감한 정보는 코드가 아닌 환경 변수에 저장

## 문서화
- 문서를 최신 상태로 유지
- 모든 주요 기능 및 구성 요소 문서화
- 새로운 개발자를 위한 설정 지침 포함
