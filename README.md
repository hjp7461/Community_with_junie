# 커뮤니티 웹 애플리케이션

## 프로젝트 소개
이 프로젝트는 Django 기반의 커뮤니티 웹 애플리케이션입니다. 사용자 관리 기능과 커뮤니티 관리 기능을 제공하며, 게시판, 카테고리, 공지사항, FAQ 등 다양한 커뮤니티 기능을 포함하고 있습니다.  

또 직접 작성한 초기 요구사항을 jetbrains junie를 통해 코드 작성, junie를 통해 요구사항 고도화 다시 코드 작성을 반복 개발하는 방식으로 개발되었습니다.  


## 주요 기능
- 사용자 관리 (회원가입, 로그인, 프로필 관리)
- 게시판 및 카테고리 구조
- 게시물 및 댓글 관리
- 신고 및 모더레이션 시스템
- 공지사항 및 FAQ 관리
- 검색 기능
- 역할 기반 권한 시스템
- 환경별 정적/미디어 파일 구성

## 디렉토리 구조
- `community/`: 커뮤니티 관련 Django 앱
  - `models.py`: 커뮤니티 모델 정의
  - `views.py`: 커뮤니티 관련 뷰 함수
  - `forms.py`: 커뮤니티 관련 폼
  - `urls.py`: 커뮤니티 관련 URL 라우팅
  - `admin.py`: 관리자 인터페이스 설정
  - `tests.py`: 테스트 코드
  - `migrations/`: 데이터베이스 마이그레이션 파일
  - `README.md`: 커뮤니티 앱 문서
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
  - `community/`: 커뮤니티 관련 템플릿
    - `board_detail.html`: 게시판 상세 페이지
    - `category_list.html`: 카테고리 목록
    - `comment_form.html`, `comment_confirm_delete.html`: 댓글 관련 템플릿
    - `faq_list.html`: FAQ 목록
    - `media_confirm_delete.html`: 미디어 삭제 확인
    - `notice_detail.html`, `notice_list.html`: 공지사항 관련 템플릿
    - `post_detail.html`, `post_form.html`, `post_confirm_delete.html`, `post_with_media_form.html`: 게시글 관련 템플릿
    - `report_form.html`, `report_success.html`: 신고 관련 템플릿
    - `search_results.html`: 검색 결과 페이지
  - `users/`: 사용자 관련 템플릿
    - `login.html`: 로그인 페이지
    - `register.html`: 회원가입 페이지
    - `profile.html`, `profile_update.html`, `user_update.html`: 프로필 관련 템플릿
    - `password_change.html`, `password_reset.html`, `password_reset_complete.html`, `password_reset_confirm.html`, `password_reset_done.html`, `password_reset_email.html`, `password_reset_subject.txt`: 비밀번호 관련 템플릿
- `users/`: 사용자 관리 Django 앱
  - `models.py`: 사용자 모델 정의
  - `views.py`: 사용자 관련 뷰 함수
  - `forms.py`: 사용자 관련 폼
  - `urls.py`: 사용자 관련 URL 라우팅
  - `admin.py`: 관리자 인터페이스 설정
  - `signals.py`: 사용자 관련 시그널 처리
  - `tests.py`: 테스트 코드
  - `migrations/`: 데이터베이스 마이그레이션 파일
- `.junie/`: 프로젝트 가이드라인 및 문서
  - `guidelines.md`: 프로젝트 가이드라인 문서
- `.venv/`: 가상 환경 디렉토리

### 주요 파일
- `manage.py`: Django 프로젝트 관리 스크립트
- `db.sqlite3`: SQLite 데이터베이스 파일
- `pyproject.toml`: 프로젝트 의존성 및 설정
- `uv.lock`: 의존성 잠금 파일
- `conftest.py`: pytest 공유 fixture 및 설정
- `pytest.ini`: pytest 설정 파일
- `README.md`: 프로젝트 README 파일

## 설치 및 설정

### 요구사항
- Python 3.8 이상
- Django 4.0 이상
- 기타 의존성은 `pyproject.toml` 파일 참조

### 환경 설정
1. `.venv`를 사용하여 가상 환경 생성
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # 또는
   .venv\Scripts\activate  # Windows
   ```

2. 이 프로젝트는 Python 패키지 매니저 `uv`를 사용합니다. 패키지 설치 시 `uv` 또는 `uv pip` 명령어를 사용해야 합니다.
   ```bash
   # 패키지 설치 예시
   uv pip install -r requirements.txt
   # 또는
   uv install -r requirements.txt
   ```

3. 데이터베이스 마이그레이션
   ```bash
   python manage.py migrate
   ```

4. 개발 서버 실행
   ```bash
   python manage.py runserver
   ```

5. 웹 브라우저에서 `http://127.0.0.1:8000/` 접속

## 개발 가이드라인

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

#### pytest 설정 및 사용법
이 프로젝트는 테스트를 위해 pytest를 사용합니다. 다음은 pytest 설정 및 사용 방법입니다:

1. **설치된 테스트 패키지**:
   - `pytest`: 테스트 프레임워크
   - `pytest-django`: Django와 pytest 통합
   - `pytest-cov`: 코드 커버리지 보고서 생성

2. **테스트 실행 방법**:
   ```bash
   # 모든 테스트 실행
   python -m pytest

   # 특정 앱의 테스트만 실행
   python -m pytest users/
   python -m pytest community/

   # 특정 테스트 파일 실행
   python -m pytest users/tests.py

   # 코드 커버리지 보고서 생성
   python -m pytest --cov=. --cov-report=html
   ```

3. **테스트 파일 구조**:
   - 테스트 파일은 `test_*.py`, `*_test.py`, 또는 `tests.py` 형식으로 작성
   - 테스트 함수는 `test_`로 시작해야 함

4. **pytest 설정 파일**:
   - `pytest.ini`: 프로젝트 루트에 위치하며 기본 설정 포함
   - `conftest.py`: 공유 fixture 및 설정 포함

5. **주요 fixture**:
   - `client`: Django 테스트 클라이언트
   - `db`: 데이터베이스 액세스 허용
   - `user_data`: 테스트 사용자 데이터
   - `create_user`: 테스트 사용자 생성

6. **데이터베이스 테스트**:
   - 데이터베이스를 사용하는 테스트에는 `@pytest.mark.django_db` 데코레이터 사용

7. **테스트 작성 가이드라인**:
   - 각 테스트는 단일 기능 또는 동작 테스트에 집중
   - 명확한 이름과 설명적인 assert 메시지 사용
   - 테스트 간 의존성 최소화

## 커뮤니티 앱 기능

### 1. 게시판/카테고리 구조

- **카테고리**: 커뮤니티의 최상위 조직 구조
  - 속성: 이름, 설명, 슬러그, 순서, 활성 상태
  - 각 카테고리는 여러 게시판을 포함할 수 있음

- **게시판**: 카테고리 내에서 조직된 토론 포럼
  - 속성: 이름, 설명, 슬러그, 순서, 활성 상태, 비공개 상태
  - 콘텐츠 모더레이션을 위한 모더레이터 할당

### 2. 신고 및 모더레이션 시스템

- **신고**: 부적절한 콘텐츠를 신고하는 시스템
  - 신고 유형: 게시물, 댓글, 사용자
  - 신고 이유: 스팸, 괴롭힘, 부적절한 콘텐츠, 불법 콘텐츠, 기타
  - 상태 추적: 대기 중, 검토 중, 해결됨, 거부됨
  - 모더레이터 할당 및 메모

### 3. 공지사항 및 FAQ 관리

- **공지사항**: 커뮤니티 공지 및 중요 정보
  - 공지 유형: 공지, 업데이트, 유지보수, 이벤트
  - 기능: 고정, 활성 상태, 날짜 범위 유효성
  - 작성자 추적 및 타임스탬프

- **FAQ**: 카테고리별로 정리된 자주 묻는 질문
  - 속성: 질문, 답변, 카테고리, 순서, 활성 상태
  - 카테고리별로 그룹화된 아코디언 인터페이스로 표시

## 역할 기반 권한 시스템

### 개요
이 프로젝트는 다음 원칙에 기반한 역할 기반 권한 시스템을 구현합니다:

1. **역할 기반 접근 제어(RBAC)**: 사용자에게 역할이 할당되고, 역할에 권한이 부여됩니다.
2. **계층적 역할**: 역할은 상위 역할로부터 권한을 상속받을 수 있습니다.
3. **최소 권한의 원칙**: 사용자는 필요한 최소한의 권한만 가져야 합니다.
4. **동적 권한**: 신뢰 수준과 임시 역할에 따라 권한이 조정될 수 있습니다.
5. **감사 및 로깅**: 보안을 위해 권한 사용이 추적되고 기록됩니다.

### 역할 계층
시스템은 다음과 같은 기본 역할을 정의합니다(권한이 증가하는 순서):

1. **게스트**: 공개 콘텐츠에 대한 읽기 전용 접근
2. **일반 사용자**: 자신의 콘텐츠를 생성하고 관리할 수 있음
3. **모더레이터**: 콘텐츠를 중재하고 사용자에게 경고할 수 있음
4. **관리자**: 콘텐츠, 사용자, 카테고리를 관리할 수 있음
5. **슈퍼 관리자**: 모든 권한을 가지고 시스템을 관리할 수 있음

### 권한 카테고리
권한은 세 가지 주요 카테고리로 나뉩니다:

1. **콘텐츠 권한**: 콘텐츠 읽기, 생성, 편집, 삭제 등
2. **사용자 관리 권한**: 사용자 보기, 경고, 일시 중지, 차단 등
3. **시스템 관리 권한**: 카테고리 관리, 시스템 설정 변경, 로그 접근 등

### 동적 권한 기능
- **신뢰 기반 권한**: 계정 나이, 활동 수준, 콘텐츠 품질, 커뮤니티 평판 등에 따라 추가 권한 획득
- **임시 역할**: 이벤트 모더레이터, 프로젝트 리더, 콘테스트 심사위원 등 특정 목적을 위한 임시 역할 할당

### 권한 시스템 사용
- 뷰에서 데코레이터 및 믹스인 사용
- 템플릿에서 필터 및 태그 사용
- 역할 관리를 위한 관리 명령어 제공

## 정적 및 미디어 파일 구성

### 개요
이 프로젝트는 배포 환경에 따라 정적 및 미디어 파일을 다르게 구성합니다:

### 구성 구조
프로젝트는 환경별 설정 파일이 있는 모듈식 설정 구조를 사용합니다:
- `config/settings/base.py`: 모든 환경에서 공유되는 공통 설정
- `config/settings/development.py`: 개발 환경 전용 설정
- `config/settings/production.py`: 프로덕션 환경 전용 설정

### 개발 환경
개발 환경에서는 정적 및 미디어 파일이 로컬에 저장됩니다:
- 정적 파일: `STATIC_URL = 'static/'`, `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- 미디어 파일: `MEDIA_URL = '/media/'`, `MEDIA_ROOT = BASE_DIR / 'media'`

### 프로덕션 환경
프로덕션 환경에서는 환경 변수를 사용하여 정적 및 미디어 파일 설정을 구성할 수 있습니다:
- 정적 파일: `STATIC_URL`, `STATIC_ROOT`, `STATICFILES_DIR` 환경 변수 사용
- 미디어 파일: `MEDIA_URL`, `MEDIA_ROOT` 환경 변수 사용

### 배포 고려사항
- 배포 환경에 적합한 환경 변수 설정
- 정적 파일의 경우 CDN 또는 별도의 정적 파일 서버 사용 가능
- 미디어 파일의 경우 AWS S3와 같은 클라우드 스토리지 서비스 사용 가능
- `python manage.py collectstatic` 실행하여 모든 정적 파일을 `STATIC_ROOT` 디렉토리에 수집
- 웹 서버(예: Nginx)가 적절한 디렉토리에서 정적 및 미디어 파일을 제공하도록 구성

## 배포
- 프로젝트는 개발 및 프로덕션 환경에 대한 별도의 설정이 있음
- 프로덕션 서버에 배포할 때 프로덕션 설정 사용
- 모든 민감한 정보는 코드가 아닌 환경 변수에 저장

## 문서화
- 문서를 최신 상태로 유지
- 모든 주요 기능 및 구성 요소 문서화
- 새로운 개발자를 위한 설정 지침 포함
