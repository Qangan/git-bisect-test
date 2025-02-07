import os
import subprocess
import sys

def bisect(start_commit: str, end_commit: str, test_command: str, rep_folder: str) -> str:
    if not os.path.isdir(rep_folder):
        print(f"{rep_folder} is not found")
        exit(1)

    commit_range = f"{start_commit}..{end_commit}"
    log_output = subprocess.check_output(f"git rev-list --ancestry-path {commit_range}", cwd=rep_folder, shell=True).decode().strip()
    commits = log_output.split("\n")[::-1]

    left = 0
    right = len(commits) - 1

    while left < right:
        mid = (left + right) // 2
        mid_commit = commits[mid]

        print(f"Checking {mid_commit}")
        result = subprocess.run(f"git checkout --quiet {mid_commit}", cwd=rep_folder, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        result = subprocess.run(test_command, cwd=rep_folder, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode
        if result == 0:
            print(f"{mid_commit} is good")
            left = mid + 1
        else:
            print(f"{mid_commit} is bad")
            right = mid

    bad_commit = commits[left]
    return bad_commit


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("usage: python bisect.py <start-commit> <end-commit> <check_command> <rep_folder>")
        sys.exit(1)

    start_commit = sys.argv[1]
    end_commit = sys.argv[2]
    test_command = sys.argv[3]
    i = 4
    if test_command[0] == '"':
        while sys.argv[i][-1] != '"':
            test_command += ' ' + sys.argv[i]
    rep_folder = sys.argv[i]

    print("Found: ", bisect(start_commit, end_commit, test_command, rep_folder))
