#!/bin/bash
# ===========================================
# DOT System - Pre-Installation (Linux/Offline)
# Ubuntu 22.04/24.04 기준
# 관리자 권한 필요: sudo ./pre_install.sh
# ===========================================

set -e

if [ "$EUID" -ne 0 ]; then
    echo "[ERROR] Root privileges required."
    echo "        Run: sudo ./pre_install.sh"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PREREQ_DIR="$SCRIPT_DIR/prerequisites/linux"

echo "========================================================="
echo "       DOT System - Pre-Installation (Linux)"
echo "========================================================="
echo ""

echo "[1/4] Checking system status..."
echo ""

# Check NVIDIA driver
NVIDIA_INSTALLED=0
if nvidia-smi &> /dev/null; then
    echo "   [OK] NVIDIA driver is installed."
    NVIDIA_INSTALLED=1
else
    echo "   [  ] NVIDIA driver is not installed."
fi

# Check Docker
DOCKER_INSTALLED=0
if command -v docker &> /dev/null; then
    echo "   [OK] Docker is installed."
    DOCKER_INSTALLED=1
else
    echo "   [  ] Docker is not installed."
fi

# Check NVIDIA Container Toolkit
TOOLKIT_INSTALLED=0
if dpkg -l nvidia-container-toolkit &> /dev/null 2>&1; then
    echo "   [OK] NVIDIA Container Toolkit is installed."
    TOOLKIT_INSTALLED=1
else
    echo "   [  ] NVIDIA Container Toolkit is not installed."
fi

echo ""

if [ $NVIDIA_INSTALLED -eq 1 ] && [ $DOCKER_INSTALLED -eq 1 ] && [ $TOOLKIT_INSTALLED -eq 1 ]; then
    echo "   All required software is already installed!"
    echo ""
    echo "   You can now run: ./install.sh"
    exit 0
fi

echo "========================================================="
echo "       Installation Plan"
echo "========================================================="
echo ""
[ $NVIDIA_INSTALLED -eq 0 ] && echo "   [1] NVIDIA Driver"
[ $DOCKER_INSTALLED -eq 0 ] && echo "   [2] Docker Engine"
[ $TOOLKIT_INSTALLED -eq 0 ] && echo "   [3] NVIDIA Container Toolkit"
echo ""

read -p "Proceed with installation? [Y/n]: " PROCEED
if [[ "$PROCEED" =~ ^[Nn]$ ]]; then
    echo "Installation cancelled."
    exit 0
fi

# ==========================================
# Install NVIDIA Driver
# ==========================================
if [ $NVIDIA_INSTALLED -eq 0 ]; then
    echo ""
    echo "[2/4] Installing NVIDIA Driver..."
    echo ""

    NVIDIA_RUN=$(find "$PREREQ_DIR" -name "NVIDIA-Linux-*.run" 2>/dev/null | head -1)

    if [ -z "$NVIDIA_RUN" ]; then
        echo "[ERROR] NVIDIA driver .run file not found!"
        echo "        Expected: $PREREQ_DIR/NVIDIA-Linux-*.run"
        echo ""
        echo "        Download from: https://www.nvidia.com/Download/index.aspx"
        echo "        Place the .run file in: $PREREQ_DIR/"
        exit 1
    fi

    chmod +x "$NVIDIA_RUN"
    echo "       Installing: $(basename $NVIDIA_RUN)"
    "$NVIDIA_RUN" --silent --no-questions

    echo "   [OK] NVIDIA Driver installed."
    NEED_REBOOT=1
fi

# ==========================================
# Install Docker Engine
# ==========================================
if [ $DOCKER_INSTALLED -eq 0 ]; then
    echo ""
    echo "[3/4] Installing Docker Engine..."
    echo ""

    DOCKER_DEBS="$PREREQ_DIR/docker"

    if [ ! -d "$DOCKER_DEBS" ] || [ -z "$(ls $DOCKER_DEBS/*.deb 2>/dev/null)" ]; then
        echo "[ERROR] Docker .deb packages not found!"
        echo "        Expected: $DOCKER_DEBS/*.deb"
        echo ""
        echo "        Download from: https://download.docker.com/linux/ubuntu/dists/"
        echo "        Required packages:"
        echo "          - containerd.io_*.deb"
        echo "          - docker-ce_*.deb"
        echo "          - docker-ce-cli_*.deb"
        echo "          - docker-compose-plugin_*.deb"
        echo "        Place them in: $DOCKER_DEBS/"
        exit 1
    fi

    echo "       Installing Docker packages..."
    dpkg -i "$DOCKER_DEBS"/*.deb || true
    apt-get install -f -y 2>/dev/null || true

    systemctl enable docker
    systemctl start docker

    # Add current user to docker group
    ACTUAL_USER="${SUDO_USER:-$USER}"
    usermod -aG docker "$ACTUAL_USER"

    echo "   [OK] Docker Engine installed."
    echo "   [!] User '$ACTUAL_USER' added to docker group."
fi

# ==========================================
# Install NVIDIA Container Toolkit
# ==========================================
if [ $TOOLKIT_INSTALLED -eq 0 ]; then
    echo ""
    echo "[4/4] Installing NVIDIA Container Toolkit..."
    echo ""

    TOOLKIT_DEBS="$PREREQ_DIR/nvidia-container-toolkit"

    if [ ! -d "$TOOLKIT_DEBS" ] || [ -z "$(ls $TOOLKIT_DEBS/*.deb 2>/dev/null)" ]; then
        echo "[ERROR] NVIDIA Container Toolkit .deb packages not found!"
        echo "        Expected: $TOOLKIT_DEBS/*.deb"
        echo ""
        echo "        Download from: https://nvidia.github.io/libnvidia-container/stable/deb/"
        echo "        Required packages:"
        echo "          - nvidia-container-toolkit_*.deb"
        echo "          - libnvidia-container1_*.deb"
        echo "          - libnvidia-container-tools_*.deb"
        echo "        Place them in: $TOOLKIT_DEBS/"
        exit 1
    fi

    echo "       Installing NVIDIA Container Toolkit packages..."
    dpkg -i "$TOOLKIT_DEBS"/*.deb || true
    apt-get install -f -y 2>/dev/null || true

    # Configure Docker to use NVIDIA runtime
    nvidia-ctk runtime configure --runtime=docker
    systemctl restart docker

    echo "   [OK] NVIDIA Container Toolkit installed."
fi

# ==========================================
# Complete
# ==========================================
echo ""
echo "========================================================="
echo "       Pre-Installation Complete"
echo "========================================================="
echo ""

if [ "${NEED_REBOOT:-}" = "1" ]; then
    echo "[!] Please REBOOT your computer."
    echo ""
    echo "After reboot:"
    echo "  1. Run: ./install.sh"
    echo ""
    read -p "Reboot now? [Y/n]: " DO_REBOOT
    if [[ ! "$DO_REBOOT" =~ ^[Nn]$ ]]; then
        reboot
    fi
else
    echo "Next steps:"
    echo "  1. Log out and log back in (for docker group)"
    echo "  2. Run: ./install.sh"
    echo ""
fi
