#!/usr/bin/env python3

import os
import sys
import shutil
import platform
import argparse
import subprocess


class Logger:
    def __init__(self, filepath):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        except Exception:
            pass  # fail silently here, it will crash explicitly on the open() call

        self.terminal = sys.stdout
        self.log = open(filepath, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        pass


def exe(cmd, cwd=None, capture=False, shell=False):
    # runs commands, prints them out
    c = " ".join(cmd) if isinstance(cmd, list) else cmd
    print(f"Running command - [{c}]")
    try:
        if capture:
            res = subprocess.run(
                cmd,
                cwd=cwd,
                shell=shell,
                check=True,
                capture_output=True,
                text=True,
            )
            return res.stdout.strip()
        else:
            subprocess.run(cmd, cwd=cwd, shell=shell, check=True)
            return None
    except subprocess.CalledProcessError as e:
        print(f"The command failed with below error : \n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"command failed with exception : \n{e}")
        sys.exit(1)


def tool_exists(name):
    # check if a command line tool exists
    return shutil.which(name) is not None


_GIT_REPO = "https://github.com/saur2729/devops_challenge.git"


def setup_git():
    if tool_exists("git"):
        print("Git is already installed.")
        return

    print("Couldn't find git installed locally, installing it now...")
    sys_type = platform.system()

    try:
        if sys_type == "Linux":
            # try apt first
            if tool_exists("apt"):
                exe(["sudo", "apt", "update"])
                exe(["sudo", "apt", "install", "-y", "git"])
            elif tool_exists("yum"):
                exe(["sudo", "yum", "install", "-y", "git"])
            else:
                print(
                    "You need apt or yum to install git on linux, please fix"
                    " and rerun the script. Exiting now..."
                )
                sys.exit(1)
            print(f"Git installed successfully at path [{shutil.which('git')}].")

        elif sys_type == "Darwin":
            if tool_exists("brew"):
                exe(["brew", "install", "git"])
            else:
                print(
                    "You need brew to install git on mac, please fix and rerun"
                    " the script. Exiting now..."
                )
                sys.exit(1)
            print(f"Git installed successfully at path [{shutil.which('git')}].")

        else:
            print(
                f"The current OS type is not Linux/Darwin. Please install "
                f"git manually for os : [{sys_type}]"
            )
            sys.exit(1)

    except Exception as e:
        print(f"Git setup failed with exception: \n{e}")
        sys.exit(1)


def pull_repo(target_dir):
    # clone if missing, pull if existing
    if os.getcwd() == target_dir:
        if os.path.isdir(".git"):
            exe(["git", "pull"])

    elif os.path.isdir(os.path.join(target_dir, ".git")):
        print("The repo already exists, doing a git pull")
        exe(["git", "pull"], cwd=target_dir)

    else:
        print(f"Cloning the repo into [{target_dir}]")
        exe(["git", "clone", _GIT_REPO, target_dir])

    print(f"Successfully pulled the git repo at [{target_dir}]")


def parse_args():
    parser = argparse.ArgumentParser(description="Installation Phase")
    parser.add_argument(
        "-w", "--work_dir", help="Target working directory", default=None
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # figure out where the repo should go
    if args.work_dir:
        target_dir = os.path.abspath(args.work_dir)
    elif os.path.exists(".git") and os.path.exists("package.json"):
        # looks like we're already inside the repo
        target_dir = os.getcwd()
    else:
        target_dir = os.path.abspath(os.path.join(os.getcwd(), "devops_challenge"))

    sys.stdout = Logger(os.path.join(os.getcwd(), "install_exec.log"))
    sys.stderr = sys.stdout

    print(f"Using work dir - [{target_dir}]")

    print("\n--- Setting up git ---")
    setup_git()

    print("--- Pulling the git repo ---")
    pull_repo(target_dir)

    # move on to the actual app setup
    setup_script = os.path.join(target_dir, "setup.py")
    if os.path.exists(setup_script):
        print("Starting setup.py script now...")
        exe([sys.executable, "setup.py", "-w", target_dir], cwd=target_dir)
    else:
        print(f"Setup script is missing at [{setup_script}]")

    # Move the log into the final logs/ folder so everything is together
    local_log = os.path.join(os.getcwd(), "install_exec.log")
    dest_log = os.path.join(target_dir, "logs", "install_exec.log")

    if os.path.exists(local_log) and local_log != dest_log:
        try:
            sys.stdout.log.close()
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            os.makedirs(os.path.join(target_dir, "logs"), exist_ok=True)
            shutil.move(local_log, dest_log)
        except Exception:
            pass


if __name__ == "__main__":
    main()
