#!/bin/bash

REPO_URL="https://github.com/swft-chain/devops-challenge-sh.git"
REPO_DIR="/home/saurabh/projects/devops/devops-challenge-sh"

# TODO: Check Git installation Status

# Step 1: Clone or update the repository
if [ -d "$REPO_DIR/.git" ]; then
    echo "[+] Repository exists. Pulling latest changes..."
    cd "$REPO_DIR" && git pull
else
    # if git installed locally ?
    if [ -f "/usr/bin/git" ]; then
        echo "Locally Git is installed, will continue to clone repo"
    else
        # install git app locally 
        # TODO : Check passwd manager here ? ## Assuming root here
        # TODO : Check OS type and opt for different installation cmdline
        sudo apt update && sudo apt install git
        echo "Git installed with version ${git --version}"
    fi

    echo "[+] Cloning repository..."
    git clone "$REPO_URL" "$REPO_DIR"
    cd "$REPO_DIR" || { echo "Failed to enter directory"; exit 1; }
fi

# Prepare logs directory
mkdir -p logs

# Step 2: Make scripts executable
echo "[+] Granting execution permissions..."
chmod +x setup.sh

# Step 3: Run setup.sh
echo "[+] Running setup.sh..."
./setup.sh