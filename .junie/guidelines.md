# 프로젝트 가이드라인

## 프로젝트 개요
이 프로젝트는 Django 기반 웹 애플리케이션입니다. 프로젝트는 표준 Django 프로젝트 구조와 규칙을 따릅니다.  
또 직접 작성한 초기 요구사항을 jetbrains junie를 통해 코드 작성, junie를 통해 요구사항 고도화 다시 코드 작성을 반복 개발하는 방식으로 개발되었습니다.  

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
  - `permission_system.md`: 권한 시스템 문서
  - `static_media_configuration.md`: 정적 및 미디어 파일 설정 문서
  - `tasks.md`: 프로젝트 작업 목록
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
    - `permission_badge.html`: 권한 배지 템플릿
- `users/`: 사용자 관리 Django 앱
  - `models.py`: 사용자 모델 정의
  - `views.py`: 사용자 관련 뷰 함수
  - `forms.py`: 사용자 관련 폼
  - `urls.py`: 사용자 관련 URL 라우팅
  - `admin.py`: 관리자 인터페이스 설정
  - `signals.py`: 사용자 관련 시그널 처리
  - `middleware.py`: 사용자 관련 미들웨어
  - `permissions.py`: 권한 관련 코드
  - `tests.py`: 테스트 코드
  - `migrations/`: 데이터베이스 마이그레이션 파일
  - `management/`: 커스텀 관리 명령어
    - `commands/`: 관리 명령어 모듈
      - `manage_roles.py`: 사용자 역할 관리 명령어
  - `templatetags/`: 커스텀 템플릿 태그
    - `user_tags.py`: 사용자 관련 템플릿 태그
- `logs/`: 로그 파일
  - `permission_audit.log`: 권한 감사 로그
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

## 배포
- 프로젝트는 개발 및 프로덕션 환경에 대한 별도의 설정이 있음
- 프로덕션 서버에 배포할 때 프로덕션 설정 사용
- 모든 민감한 정보는 코드가 아닌 환경 변수에 저장

## 문서화
- 문서를 최신 상태로 유지
- 모든 주요 기능 및 구성 요소 문서화
- 새로운 개발자를 위한 설정 지침 포함
