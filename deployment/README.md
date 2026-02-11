# DOT System - Offline Deployment Package

Air-gapped(폐쇄망) 환경을 위한 오프라인 설치 패키지 구조입니다.

## 패키지 구조

```
deployment/
├── prerequisites/                    # 사전 설치 파일 (직접 다운로드 필요)
│   ├── NVIDIADriver.exe             # [Windows] NVIDIA Game Ready Driver
│   ├── Microsoft.WSL_*.msixbundle   # [Windows] WSL2 설치 패키지
│   ├── Ubuntu2404-*.AppxBundle      # [Windows] Ubuntu 24.04 for WSL
│   ├── DockerDesktopInstaller.exe   # [Windows] Docker Desktop
│   └── linux/                       # [Linux] 오프라인 설치 패키지
│       ├── NVIDIA-Linux-*.run       #   NVIDIA 드라이버 (.run)
│       ├── docker/                  #   Docker Engine .deb 패키지
│       │   ├── containerd.io_*.deb
│       │   ├── docker-ce_*.deb
│       │   ├── docker-ce-cli_*.deb
│       │   └── docker-compose-plugin_*.deb
│       └── nvidia-container-toolkit/
│           ├── nvidia-container-toolkit_*.deb
│           ├── libnvidia-container1_*.deb
│           └── libnvidia-container-tools_*.deb
│
├── images/                           # Docker 이미지 (docker save로 생성)
│   ├── backend.tar                  # dot-project-backend:latest
│   ├── frontend.tar                 # dot-project-frontend:latest
│   ├── mysql.tar                    # mysql:8.0
│   ├── redis.tar                    # redis:alpine
│   ├── worker.tar                   # dot-project-backend:latest (worker용)
│   └── comfyui.tar                  # dot-comfyui:latest
│
├── models/                           # AI 모델 파일 (직접 배치 필요)
│   ├── llm/                         # LLM 모델 (.gguf)
│   ├── embedding/hub/               # HuggingFace 임베딩 모델 (hub/ 하위 필수)
│   ├── stt/                         # Whisper STT 모델
│   ├── image/                       # ComfyUI 이미지 생성 모델
│   └── chroma_db/                   # ChromaDB 초기 데이터
│
├── config/
│   ├── .env.template                # 환경변수 템플릿
│   ├── docker-compose-master-deploy.yml
│   └── docker-compose-worker-deploy.yml
│
├── pre_install.bat                   # Windows 사전 설치 (관리자 권한)
├── pre_install.sh                    # Linux 사전 설치 (sudo 필요)
├── install.bat                       # Windows DOT 시스템 설치
├── install.sh                        # Linux DOT 시스템 설치
├── manage.sh                         # Linux 서비스 관리 도구
└── update.sh                         # 업데이트 스크립트
```

## 패키지 빌드 방법

### 1. 사전 설치 파일 다운로드

#### Windows (prerequisites/)

| 파일 | 다운로드 |
|------|---------|
| NVIDIADriver.exe | https://www.nvidia.com/Download/index.aspx (GPU 모델에 맞는 드라이버) |
| Microsoft.WSL_*.msixbundle | https://github.com/microsoft/WSL/releases |
| Ubuntu2404-*.AppxBundle | https://apps.microsoft.com 또는 MS Store에서 오프라인 패키지 |
| DockerDesktopInstaller.exe | https://www.docker.com/products/docker-desktop/ |

#### Linux (prerequisites/linux/)

| 파일 | 다운로드 |
|------|---------|
| NVIDIA-Linux-*.run | https://www.nvidia.com/Download/index.aspx (Linux 64-bit, .run 파일) |
| docker/*.deb | https://download.docker.com/linux/ubuntu/dists/ (Ubuntu 버전에 맞는 amd64 패키지) |
| nvidia-container-toolkit/*.deb | https://nvidia.github.io/libnvidia-container/stable/deb/ |

Linux Docker .deb 필수 패키지: `containerd.io`, `docker-ce`, `docker-ce-cli`, `docker-compose-plugin`
Linux NVIDIA Container Toolkit 필수 패키지: `nvidia-container-toolkit`, `libnvidia-container1`, `libnvidia-container-tools`

### 2. Docker 이미지 생성

```bash
# PC1 (Master)에서 실행
docker save dot-project-backend:latest -o images/backend.tar
docker save dot-project-frontend:latest -o images/frontend.tar
docker save mysql:8.0 -o images/mysql.tar
docker save redis:alpine -o images/redis.tar

# PC2 (Worker)에서 실행
docker save dot-project-backend:latest -o images/worker.tar
docker save dot-comfyui:latest -o images/comfyui.tar
```

### 3. AI 모델 배치

```
models/llm/              ← llama-3-Korean-Bllossom-8B-Q4_K_M.gguf
models/embedding/hub/    ← models--jhgan--ko-sbert-nli/ (hub/ 폴더 하위에 배치 필수)
models/stt/              ← faster-whisper-large-v3/
models/image/            ← unet/, clip/, vae/ (ComfyUI 모델)
```

> **주의**: 임베딩 모델은 반드시 `embedding/hub/models--jhgan--ko-sbert-nli/` 경로로 배치해야 합니다. HuggingFace 오프라인 캐시 구조를 따릅니다.

## 설치 방법 (폐쇄망 Windows PC)

### Step 1. 사전 설치 (pre_install.bat)

관리자 권한으로 실행합니다. 다음을 자동으로 설치합니다:
- NVIDIA 드라이버 (설치 시 "GeForce Experience" 체크 해제)
- WSL2 + Ubuntu 24.04
- Docker Desktop

설치 완료 후 **재부팅**합니다.

### Step 2. Docker Desktop 설정

재부팅 후:
1. Docker Desktop이 자동 시작됩니다
2. 로그인 화면에서 **"Skip"** 클릭 (계정 불필요)
3. Docker가 완전히 시작될 때까지 대기 (시스템 트레이 아이콘 확인)

### Step 3. DOT 시스템 설치 (install.bat)

#### PC1 (Master Server)
```
install.bat 실행 → "1" (Master) 선택 → IP 확인/입력
```

- 자동으로 방화벽 포트(3306, 6379, 8000, 5173)를 개방합니다
- 설치 경로: `C:\Users\[사용자명]\dot-project\`

#### PC2 (Worker Server)
```
install.bat 실행 → "2" (Worker) 선택 → Master PC의 실제 LAN IP 입력
```

> **주의**: IP는 반드시 실제 LAN IP(예: 192.168.0.x)를 입력하세요. Docker/WSL 내부 IP(172.x.x.x)를 사용하면 연결되지 않습니다.

## 설치 방법 (폐쇄망 Linux PC)

### Step 1. 사전 설치 (pre_install.sh)

root 권한으로 실행합니다. 다음을 오프라인으로 설치합니다:
- NVIDIA 드라이버 (.run 파일)
- Docker Engine (.deb 패키지)
- NVIDIA Container Toolkit (.deb 패키지)

```bash
sudo ./pre_install.sh
```

이미 설치된 항목은 자동으로 건너뜁니다. NVIDIA 드라이버를 새로 설치한 경우 **재부팅**이 필요합니다.

### Step 2. DOT 시스템 설치 (install.sh)

```bash
./install.sh
```

#### PC1 (Master Server)
- 설치 유형 "1" (Master) 선택 → IP 확인/입력
- 설치 경로: `$HOME/dot-project/`

#### PC2 (Worker Server)
- 설치 유형 "2" (Worker) 선택 → Master PC의 실제 LAN IP 입력

> **주의**: IP는 반드시 실제 LAN IP(예: 192.168.0.x)를 입력하세요. Docker 내부 IP(172.x.x.x)를 사용하면 연결되지 않습니다.

### Step 3. 서비스 관리 (manage.sh)

```bash
./manage.sh start     # 서비스 시작
./manage.sh stop      # 서비스 중지
./manage.sh restart   # 서비스 재시작 (.env 변경 반영)
./manage.sh status    # 서비스 상태 확인
./manage.sh logs      # 전체 로그 확인
./manage.sh logs backend  # 특정 서비스 로그
```

## 설치 후 확인

- Web 접속: `http://[Master-IP]:5173`
- 상태 확인: `docker compose ps`
- 로그 확인: `docker compose logs -f`
- 재시작: `docker compose down && docker compose up -d` (.env 변경 시)
- 단순 재시작: `docker compose restart` (.env 변경 없을 시)
