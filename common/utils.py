import os
import sys
import subprocess
import shutil
import datetime


class Logger:
    def __init__(self, filepath):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        except Exception:
            pass  # fail silently here, it will crash explicitly on the open() call

        self.terminal = sys.stdout
        self.log = open(filepath, "a")
        self._new_line = True

    def write(self, message):
        if not message:
            return

        # Add timestamps dynamically to each new line in the log file
        log_msg = ""
        for char in message:
            if self._new_line and char != "\n":
                log_msg += datetime.datetime.now().strftime("[%Y%m%d %H:%M:%S] ")
                self._new_line = False
            log_msg += char
            if char == "\n":
                self._new_line = True

        self.terminal.write(message)
        self.log.write(log_msg)
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
