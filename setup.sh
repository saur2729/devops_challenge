#!/bin/bash

echo "[Validator Setup] Starting setup..."

# Detect OS and install Node.js if missing
OS="$(uname -s)"

REPO_DIR="/d/projects/test_depvops/devops-challenge-sh"
log_file=${REPO_DIR}/logs/setup.log
PID_LOCK_FL=${REPO_DIR}/pid_lock/app.lock

mkdir -p ${REPO_DIR}/pid_lock


detect_and_install_node() {
    if command -v node &>/dev/null && command -v npm &>/dev/null; then
        echo "[INFO] Node.js already installed: $(node -v)" > $log_file
        echo "[INFO] npm version: $(npm -v)"
        return
    fi

    echo "[INFO] Node.js or npm not found. Attempting installation..."

    case "$OS" in
        Linux*)
            if [ -f /etc/debian_version ]; then
                echo "[INFO] Installing Node.js via apt..."
                curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
                sudo apt install -y nodejs
            elif [ -f /etc/redhat-release ]; then
                echo "[INFO] Installing Node.js via yum..."
                curl -fsSL https://rpm.nodesource.com/setup_22.x | sudo bash -
                sudo yum install -y nodejs
            else
                echo "[WARN] Unsupported Linux distro. Please install Node.js manually."
                exit 1
            fi
            ;;
        Darwin*)
            if command -v brew &>/dev/null; then
                echo "[INFO] Installing Node.js via Homebrew..."
                brew install node
            else
                echo "[ERROR] Homebrew not found. Please install Node.js manually."
                exit 1
            fi
            ;;
        MINGW*|MSYS*|CYGWIN*)
            echo "[INFO] Detected Windows (Git Bash or WSL). Please install Node.js manually from https://nodejs.org/"
            exit 1
            ;;
        *)
            echo "[ERROR] Unknown OS: $OS"
            exit 1
            ;;
    esac
}

# TODO: check node version >= 22
check_node_version() {
    # checks to verify node version should be great or equal to 22"
    node_ver="$(node --version | cut -c2-3)"
    if [ ${node_ver} -ge 22 ]; then
        echo "Node version is >= 22"
    else
        echo "Update node version to v22 "
        detect_and_install_node
    fi
}

detect_and_install_node
check_node_version

# Install dependencies
echo "[INFO] Installing Node.js dependencies..." > $log_file
npm install

# Prepare .env file
if [ ! -f .env ]; then
    if [ -f .env_example ]; then
        cp .env_example .env
        echo "[INFO] Copied .env_example to .env"
    else
        echo "[ERROR] No .env or .env_example found. Cannot continue."
        exit 1
    fi
fi

echo "[Validator Setup] Setup complete."

echo "[Validator] Starting the validator service..."

# Ensure .env exists
if [ ! -f .env ]; then
    echo "[ERROR] Missing .env file. Please run setup.sh first."
    exit 1
fi

# Run validator logic
# check if app is already running or not
if [ -f ${PID_LOCK_FL} ]; then 
    # check if its not a stale file
    app_pid=`cat ${PID_LOCK_FL}`

    echo "Old lock file exists with PID - ${app_pid}"

    # kill process if it exists
    kill -9 $app_pid # forecefully kill process
    # remove the old pid file
    rm ${PID_LOCK_FL}
fi


if [ ! -f ${PID_LOCK_FL} ]; then
    touch ${PID_LOCK_FL}
fi 


echo "[Validator] Starting Validator..."
npm start &

# add existing pid to the lock file
echo $! > ${PID_LOCK_FL}

