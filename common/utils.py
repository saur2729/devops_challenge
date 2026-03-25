import os
import sys
import subprocess
import shutil

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

def run_cmd(cmd, cwd=None, capture=False, shell=False):
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
