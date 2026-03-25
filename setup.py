#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
import platform
import signal
import argparse
from common.utils import Logger, run_cmd as sh, tool_exists


def check_node_v():
    if not tool_exists("node"):
        return 0
    try:
        ver = sh(["node", "--version"], capture=True)
        if ver.startswith("v"):
            return int(ver.split(".")[0][1:])
    except Exception:
        pass
    return 0


def prep_node():
    # node ver should be 22 or higher
    ver = check_node_v()
    if ver >= 22:
        print(f"Node has version [{ver}] which is good to go")
        return

    print("Installing nodejs....")
    os_name = platform.system()
    try:
        if os_name == "Linux":
            # try apt first, then yum
            if tool_exists("apt"):
                print("Trying to install nodejs using apt...")
                sh(
                    "curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -",
                    shell=True,
                )
                sh(["sudo", "apt", "install", "-y", "nodejs"])

            elif tool_exists("yum"):
                print("Trying to install nodejs using yum...")
                sh(
                    "curl -fsSL https://rpm.nodesource.com/setup_22.x | sudo bash -",
                    shell=True,
                )
                sh(["sudo", "yum", "install", "-y", "nodejs"])

            else:
                print(
                    "Unable to install node on this linux flavor."
                    " Please install node v22 manually"
                )
                sys.exit(1)

        elif os_name == "Darwin":
            if tool_exists("brew"):
                print("Trying to install nodejs using brew...")
                sh(["brew", "install", "node"])
            else:
                print("brew is missing, please install node v22 manually on macos")
                sys.exit(1)
        else:
            print("please install node v22 manually on windows")
    except Exception as e:
        print(f"Failed to install node with below exception: \n{e}")
        sys.exit(1)


def install_deps(base_dir):
    print("Running npm install...")

    # windows needs shell=True for npm
    needs_shell = platform.system() == "Windows"
    sh(["npm", "install"], shell=needs_shell, cwd=base_dir)

    # setup .env
    env_curr = os.path.join(base_dir, ".env")
    env_tmpl = os.path.join(base_dir, ".env_example")

    if not os.path.exists(env_curr):
        if os.path.exists(env_tmpl):
            shutil.copyfile(env_tmpl, env_curr)
            print("copied over .env_example to .env")
        else:
            print(".env_example is missing! exiting now ....")
            sys.exit(1)


def run_app(base_dir):
    logs_dir = os.path.join(base_dir, "logs")
    pid_dir = os.path.join(base_dir, "pid_lock")
    lock_file = os.path.join(pid_dir, "app.lock")
    log_file = os.path.join(logs_dir, "node_app.log")

    # make sure output dirs exist
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(pid_dir, exist_ok=True)

    if not os.path.exists(os.path.join(base_dir, ".env")):
        print("The .env file is missing, exiting now ...")
        sys.exit(1)

    # kill the old process if there's a lock file
    if os.path.isfile(lock_file):
        with open(lock_file, "r") as f:
            pid = f.read().strip()
            if pid.isdigit():
                print(f"killing old instance (pid {pid})")
                try:
                    if platform.system() == "Windows":
                        sh(["taskkill", "/F", "/T", "/PID", pid])
                    else:
                        os.kill(int(pid), signal.SIGKILL)
                except OSError:
                    print("looks like that process is already dead")
        os.remove(lock_file)

    print("starting validator in the background...")

    # popen to run it detached
    with open(log_file, "a") as f_out:
        if platform.system() == "Windows":
            proc = subprocess.Popen(
                ["node", "src/app.js"],
                cwd=base_dir,
                stdout=f_out,
                stderr=subprocess.STDOUT,
                shell=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )
        else:
            proc = subprocess.Popen(
                ["node", "src/app.js"],
                cwd=base_dir,
                stdout=f_out,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )

    # save new pid
    with open(lock_file, "w") as f:
        f.write(str(proc.pid))

    print(f"all set! running on pid {proc.pid}")


def parse_args():
    parser = argparse.ArgumentParser(description="Validator Setup (Phase 2)")
    parser.add_argument(
        "-w", "--work_dir", help="Target working directory", default=None
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # working dir should be the root of the repo here
    if args.work_dir:
        base_dir = os.path.abspath(args.work_dir)
    else:
        base_dir = os.getcwd()

    sys.stdout = Logger(os.path.join(base_dir, "logs", "setup_exec.log"))
    sys.stderr = sys.stdout

    print("--- Installing nodejs ---")
    prep_node()

    print("--- Installing dependencies ---")
    install_deps(base_dir)

    print("--- Starting the application ---")
    run_app(base_dir)


if __name__ == "__main__":
    main()
