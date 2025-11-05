try:
    from colorama import Fore, Back, Style, init
    COLORAMA_AVAILABLE = True
except Exception:
    # Define ANSI escape sequences as a fallback for modern terminals
    COLORAMA_AVAILABLE = False
    class _Ansi:
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"
        RESET = "\033[0m"

    class _AnsiBack:
        BLACK = "\033[40m"
        RED = "\033[41m"
        GREEN = "\033[42m"
        YELLOW = "\033[43m"
        BLUE = "\033[44m"
        MAGENTA = "\033[45m"
        CYAN = "\033[46m"
        WHITE = "\033[47m"

    class _AnsiStyle:
        RESET_ALL = "\033[0m"
        BRIGHT = "\033[1m"

    Fore = _Ansi()
    Back = _AnsiBack()
    Style = _AnsiStyle()
    def init(*args, **kwargs):
        return None

import time
import inspect
import os
import random
import sys


# Initialize Colorama (auto reset colors each print)
init(autoreset=True)

# Readable aliases mapped to Colorama
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT
DIM = ''
ITALIC = ''
UNDERLINE = ''

FG_GREEN = Fore.GREEN
FG_NEON = Fore.GREEN
FG_AMBER = Fore.YELLOW
FG_CYAN = Fore.CYAN
FG_MAGENTA = Fore.MAGENTA
FG_RED = Fore.RED
FG_YELLOW = Fore.YELLOW
FG_WHITE = Fore.WHITE
FG_GREY = Fore.WHITE


def enable_ansi_on_windows():
    # Colorama handles cross-platform color support; keep for compatibility.
    return


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def type_out(text: str, delay: float = 0.01, end: str = "\n"):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print(end, end="")


def retro_frame(lines, title="System Programming Project By Abdullah"):
    width = max(len(line) for line in lines + [title]) + 4
    top = f"{FG_NEON}+{'-' * (width - 2)}+{RESET}"
    ttl = f"{FG_NEON}| {BOLD}{title:{' '}^{width-4}}{RESET}{FG_NEON} |{RESET}"
    sep = f"{FG_NEON}+{'=' * (width - 2)}+{RESET}"
    print(top)
    print(ttl)
    print(sep)
    for line in lines:
        print(f"{FG_NEON}| {FG_GREEN}{line:{' '}<{width-4}}{FG_NEON} |{RESET}")
    print(top)


CAT_OK = rf"""
{FG_NEON}  /\_/\  {FG_GREEN}Purrr-fect!
{FG_NEON} ( o.o ) {FG_AMBER}Correct answer!
{FG_NEON}  > ^ <  {FG_CYAN}+1 point{RESET}
"""

CAT_BAD = rf"""
{FG_RED}  /\_/\
 ( x.x )  gitgud!
  > ^ <   Try again.{RESET}
"""


def banner():
    art = [
        f"{FG_AMBER}{BOLD} Prince Mohammed Bin Fahad University{RESET}",
        f"{FG_NEON}{BOLD}   /\\_/\\   {FG_AMBER}System Programming Project",
        f"{FG_NEON}{BOLD}  ( o . o ) {FG_AMBER}By Abdullah",
        f"{FG_NEON}{BOLD}   >  ^  <  {FG_CYAN}Kali + Basics Retro Quiz{RESET}",
    ]
    for line in art:
        type_out(line, delay=0.01)
    print()


class Question:
    def __init__(self, prompt: str, choices: list[str], answer: str, explain: str = "", difficulty: int = 1):
        self.prompt = prompt
        self.choices = choices
        self.answer = answer.upper().strip()
        self.explain = explain
        self.difficulty = difficulty

    def ask(self, qnum: int, total: int) -> bool:
        print(f"{FG_AMBER}{BOLD}Q{qnum}/{total}:{RESET} {FG_WHITE}{self.prompt}{RESET}")
        for ch in self.choices:
            print(f"   {FG_CYAN}{ch}{RESET}")
        print(f"{FG_GREY}(Type A, B, C, or D then press Enter){RESET}")
        while True:
            ans = input(f"{FG_NEON}> {RESET}").strip().upper()
            if ans in {"A", "B", "C", "D"}:
                break
            print(f"{FG_GREY}Please enter A, B, C, or D.{RESET}")
        correct = ans == self.answer
        if correct:
            print(CAT_OK)
        else:
            print(CAT_BAD)
            print(f"{FG_YELLOW}Correct answer: {self.answer}{RESET}")
        if self.explain:
            print(f"{FG_GREY}{self.explain}{RESET}")
        print()
        return correct


class FreeQuestion:
    def __init__(self, prompt: str, acceptable: list[str], explain: str = "", difficulty: int = 1):
        self.prompt = prompt
        self.acceptable = [a.strip().lower() for a in acceptable]
        self.explain = explain
        self.difficulty = difficulty

    def ask(self, qnum: int, total: int) -> bool:
        print(f"{FG_AMBER}{BOLD}Q{qnum}/{total}:{RESET} {FG_WHITE}{self.prompt}{RESET}")
        print(f"{FG_GREY}(Type your answer then press Enter){RESET}")
        ans = input(f"{FG_NEON}> {RESET}").strip().lower()
        correct = ans in self.acceptable
        if correct:
            print(CAT_OK)
        else:
            print(CAT_BAD)
            key = self.acceptable[0] if self.acceptable else ""
            if key:
                print(f"{FG_YELLOW}One correct answer: {key}{RESET}")
        if self.explain:
            print(f"{FG_GREY}{self.explain}{RESET}")
        print()
        return correct

# This code will build the questions for the game 
def build_questions() -> list[Question]:
    # This is where the questions will be stored
    q = []
    # This is where the questions will be added
    q.append(Question(
        "Which command prints the current working directory?",
        ["A) cd", "B) pwd", "C) ls", "D) whoami"],
        "B",
        "pwd outputs the present working directory.",
        # This is where the difficulty of the question is set
        difficulty=1,
    ))
    q.append(Question(
        "Change directory into /etc from anywhere:",
        ["A) cd /etc", "B) ls /etc", "C) pwd /etc", "D) open /etc"],
        "A",
        "cd changes the current directory.",
        difficulty=1,
    ))
    q.append(Question(
        "List files, including hidden ones:",
        ["A) ls -a", "B) ls -l", "C) dir -h", "D) tree -a"],
        "A",
        "ls -a shows all entries including dotfiles.",
        difficulty=1,
    ))
    q.append(Question(
        "Create a directory named hacks:",
        ["A) touch hacks", "B) mkdir hacks", "C) make hacks", "D) newdir hacks"],
        "B",
        "mkdir creates directories.",
        difficulty=1,
    ))
    q.append(Question(
        "Remove a file notes.txt:",
        ["A) rm notes.txt", "B) rmdir notes.txt", "C) deldir notes.txt", "D) erase notes.txt"],
        "A",
        "rm removes files; rmdir removes empty directories.",
        difficulty=1,
    ))
    q.append(Question(
        "Show the contents of a file report.log:",
        ["A) touch report.log", "B) cat report.log", "C) run report.log", "D) vi report.log"],
        "B",
        "cat prints file contents to stdout.",
        difficulty=1,
    ))
    q.append(Question(
        "Find lines containing 'root' in /etc/passwd:",
        ["A) grep root /etc/passwd", "B) find root /etc/passwd", "C) search root /etc/passwd", "D) cat -g root /etc/passwd"],
        "A",
        "grep searches for patterns in text.",
        difficulty=2,
    ))
    q.append(Question(
        "Install package nmap (Debian/Kali):",
        ["A) sudo install nmap", "B) sudo apt install nmap", "C) apt-get make nmap", "D) pkg nmap"],
        "B",
        "apt install fetches and installs packages.",
        difficulty=2,
    ))
    q.append(Question(
        "Show your username:",
        ["A) user", "B) id -u", "C) whoami", "D) echo $name"],
        "C",
        "whoami prints the effective username.",
        difficulty=1,
    ))
    q.append(Question(
        "Show network interfaces and addresses on Kali (modern):",
        ["A) ifconfig -all", "B) ip a", "C) netstat -i", "D) route print"],
        "B",
        "ip a (ip address) shows addresses; ifconfig is deprecated on many systems.",
        difficulty=2,
    ))
    q.append(Question(
        "Which command changes a file's permissions?",
        ["A) chmod", "B) chown", "C) chperm", "D) setperm"],
        "A",
        "chmod modifies permission bits.",
        difficulty=2,
    ))
    q.append(Question(
        "Which command changes a file's owner?",
        ["A) chmod", "B) chown", "C) ownset", "D) setuid"],
        "B",
        "chown changes ownership.",
        difficulty=2,
    ))
    q.append(Question(
        "Get help/man page for grep:",
        ["A) grep --open", "B) help grep", "C) man grep", "D) info open grep"],
        "C",
        "man shows manual pages.",
        difficulty=1,
    ))
    q.append(Question(
        "Show last 10 lines of a file:",
        ["A) head file", "B) tail file", "C) last file", "D) end file"],
        "B",
        "tail shows the end of files; head shows the beginning.",
        difficulty=1,
    ))
    # Programming basics
    q.append(Question(
        "In an if-statement, which evaluates to True in Python?",
        ["A) 0", "B) ''", "C) []", "D) 42"],
        "D",
        "Non-zero numbers are truthy; 0, empty strings, and empty lists are falsy.",
        difficulty=2,
    ))
    q.append(Question(
        "Complete the for-loop to iterate 5 times (0..4):",
        ["A) for i in range(5):", "B) for i in range(1,5):", "C) for i in [5]:", "D) for i in range(0,6):"],
        "A",
        "range(5) yields 0,1,2,3,4.",
        difficulty=2,
    ))
    q.append(Question(
        "Which syntax is correct for an if/else in Bash?",
        ["A) if cond then; ... fi", "B) if (cond) { ... }", "C) if cond: ... end", "D) if cond do ... end"],
        "A",
        "Classic POSIX sh/bash form: if condition; then ... fi.",
        difficulty=3,
    ))
    q.append(Question(
        "Which operator compares equality in Python?",
        ["A) =", "B) ==", "C) ===", "D) eq"],
        "B",
        "= assigns; == compares equality.",
        difficulty=1,
    ))
    q.append(Question(
        "Which loop breaks early in both Bash and Python?",
        ["A) halt", "B) stop", "C) break", "D) exit"],
        "C",
        "break exits the nearest loop.",
        difficulty=1,
    ))
    # Free-form (short answer / code-ish) basics
    q.append(FreeQuestion(
        "Command to print the working directory:",
        ["pwd"],
        "Short answer expected: pwd",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Change directory to /var/log:",
        ["cd /var/log"],
        "Use an absolute path.",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "List all files including hidden (short):",
        ["ls -a"],
        "-a shows dotfiles.",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Show a long listing with human sizes:",
        ["ls -lh", "ls -alh", "ls -lah"],
        "-l long, -h human sizes; including -a is also acceptable.",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Create directory named tools:",
        ["mkdir tools"],
        "",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Remove file tmp.txt:",
        ["rm tmp.txt"],
        "",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Remove directory empty_dir:",
        ["rmdir empty_dir"],
        "rmdir works for empty directories.",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Show first 5 lines of file.txt:",
        ["head -n 5 file.txt", "head -5 file.txt"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Search 'error' in syslog:",
        ["grep error /var/log/syslog", "grep -i error /var/log/syslog"],
        "-i ignores case (optional).",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Count lines in access.log:",
        ["wc -l access.log"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Show current user:",
        ["whoami"],
        "",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Show IP addresses with ip tool:",
        ["ip a", "ip address"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Show routing table with ip:",
        ["ip r", "ip route"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Make a new empty file notes.txt:",
        ["touch notes.txt"],
        "",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Show manual page for chmod:",
        ["man chmod"],
        "",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Change file perms to rwxr-xr-x (octal):",
        ["chmod 755 file", "chmod 755 file.txt"],
        "Use sample name 'file' or 'file.txt' acceptable.",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "Change owner of file.txt to root:",
        ["sudo chown root file.txt", "chown root file.txt"],
        "Might require sudo.",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "Install nmap on Debian/Kali:",
        ["sudo apt install nmap", "apt install nmap"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Update package lists:",
        ["sudo apt update", "apt update"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Upgrade packages:",
        ["sudo apt upgrade", "apt upgrade"],
        "",
        difficulty=2,
    ))
    # Python basics, short answers
    q.append(FreeQuestion(
        "Python: print Hello World (exact):",
        ["print('hello world')", 'print("hello world")'],
        "Case of Hello not required here.",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Python: for loop 0..4 one line:",
        ["for i in range(5):"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Python: if x equals 10 (exact condition):",
        ["if x == 10:", "if (x == 10):"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Python: break out of loop keyword:",
        ["break"],
        "",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Python: continue keyword:",
        ["continue"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Bash: list files in current dir:",
        ["ls"],
        "",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Bash: print text hello:",
        ["echo hello", "echo 'hello'", 'echo "hello"'],
        "",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Bash: run script file.sh (assume executable):",
        ["./file.sh"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Bash: variable PATH expansion symbol ($VAR):",
        ["$PATH"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Find files named secrets.txt under / (simple):",
        ["find / -name secrets.txt"],
        "",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "Replace 'foo' with 'bar' in a file using sed (in-place, GNU):",
        ["sed -i 's/foo/bar/g' file.txt", 'sed -i "s/foo/bar/g" file.txt'],
        "",
        difficulty=4,
    ))
    q.append(FreeQuestion(
        "Show processes (short):",
        ["ps", "ps aux", "top", "htop"],
        "Any is acceptable.",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Check open listening ports (one tool):",
        ["ss -tuln", "netstat -tuln"],
        "",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "Archive dir logs to logs.tar using tar:",
        ["tar -cf logs.tar logs"],
        "",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "Extract logs.tar:",
        ["tar -xf logs.tar"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Compress file.txt to file.txt.gz:",
        ["gzip file.txt"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Show disk usage human-readable:",
        ["df -h"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Show folder size of current dir human-readable:",
        ["du -sh ."],
        "",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "Print only lines 10..20 of file.txt using sed:",
        ["sed -n '10,20p' file.txt", 'sed -n "10,20p" file.txt'],
        "",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "Head of file: 3 lines:",
        ["head -n 3 file.txt", "head -3 file.txt"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Tail of file: 2 lines:",
        ["tail -n 2 file.txt", "tail -2 file.txt"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Show environment variables command:",
        ["env", "printenv"],
        "",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Export variable FOO=bar in Bash:",
        ["export FOO=bar"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Run Python 3 REPL:",
        ["python3", "python"],
        "Either may work depending on system.",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Python: define function hello() no body (one-liner header):",
        ["def hello():"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Python: list literal with 1,2,3:",
        ["[1, 2, 3]", "[1,2,3]"],
        "",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Python: dict with keys a:1, b:2:",
        ["{'a': 1, 'b': 2}", '{"a": 1, "b": 2}'],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Bash: for i in 1..3 echo i (brace expansion):",
        ["for i in {1..3}; do echo $i; done"],
        "",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "Bash: if file exists test (file.txt):",
        ["if [ -f file.txt ]; then echo yes; fi"],
        "",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "Bash: make script executable file.sh:",
        ["chmod +x file.sh"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Show date/time:",
        ["date"],
        "",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Current calendar month:",
        ["cal"],
        "",
        difficulty=1,
    ))
    # networking/security light
    q.append(FreeQuestion(
        "Ping 1.1.1.1 once:",
        ["ping -c 1 1.1.1.1", "ping -n 1 1.1.1.1"],
        "-c is Linux/mac, -n is Windows.",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "DNS lookup example for example.com (one tool):",
        ["dig example.com", "nslookup example.com"],
        "",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "HTTP GET with curl to example.com:",
        ["curl http://example.com", "curl -s http://example.com"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Download file with wget:",
        ["wget URL"],
        "Use 'URL' literally here.",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Run nmap quick scan against 127.0.0.1:",
        ["nmap -T4 -F 127.0.0.1", "nmap 127.0.0.1"],
        "",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "Show kernel and OS info (Linux):",
        ["uname -a"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Print current shell:",
        ["echo $SHELL"],
        "",
        difficulty=2,
    ))
    # more Python smalls
    q.append(FreeQuestion(
        "Python: list comprehension squares 0..4:",
        ["[i*i for i in range(5)]", "[i**2 for i in range(5)]"],
        "",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "Python: length of list x (len):",
        ["len(x)"],
        "",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Python: open file.txt for reading (one-liner):",
        ["open('file.txt')", 'open("file.txt")'],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Python: integer division 7 // 2 result keyword (operator):",
        ["//"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Show hidden files only (pattern .*) with ls:",
        ["ls -d .*"],
        "",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "Print current path variable in Bash:",
        ["echo $PATH"],
        "",
        difficulty=1,
    ))
    q.append(FreeQuestion(
        "Create symbolic link ln -s target linkname:",
        ["ln -s target linkname"],
        "",
        difficulty=3,
    ))
    q.append(FreeQuestion(
        "Copy file a to b preserving attributes:",
        ["cp -a a b"],
        "",
        difficulty=2,
    ))
    q.append(FreeQuestion(
        "Move file a to folder dir/:",
        ["mv a dir/"],
        "",
        difficulty=1,
    ))
    # Order questions from easiest to hardest
    q.sort(key=lambda item: getattr(item, 'difficulty', 3))
    return q


def press_enter():
    input(f"{FG_GREY}Press Enter to continue...{RESET}")


def run_quiz():
    enable_ansi_on_windows()
    clear_screen()
    banner()
    lines = [
        "Answer questions to earn points.",
        "MCQ: type A/B/C/D. Some are short answers: type the command or code.",
        "Get it right to see the cat!",
    ]
    retro_frame(lines)
    print()
    time.sleep(0.9)

    all_q = build_questions()
    QUESTIONS_PER_RUN = 20
    total_to_ask = min(len(all_q), QUESTIONS_PER_RUN) if QUESTIONS_PER_RUN else len(all_q)
    # Take the first N (already sorted by difficulty)
    questions = all_q[:total_to_ask]

    score = 0
    for i, q in enumerate(questions, start=1):
        correct = q.ask(i, total_to_ask)
        if correct:
            score += 1
        time.sleep(0.3)

    print(f"{FG_AMBER}{BOLD}Quiz Complete!{RESET}")
    print(f"{FG_CYAN}Score: {score}/{total_to_ask}{RESET}")
    if score == total_to_ask:
        print(f"{FG_NEON}{BOLD}Flawless victory!{RESET}")
    elif score >= total_to_ask * 0.75:
        print(f"{FG_GREEN}Great job!{RESET}")
    elif score >= total_to_ask * 0.5:
        print(f"{FG_YELLOW}Not bad—keep practicing!{RESET}")
    else:
        print(f"{FG_RED}Give it another go!{RESET}")

    print()
    print(f"{FG_GREY}R) Replay    Q) Quit{RESET}")
    while True:
        choice = input(f"{FG_NEON}> {RESET}").strip().upper()
        if choice in {"R", "Q"}:
            break
        print(f"{FG_GREY}Type R to replay or Q to quit.{RESET}")
    if choice == "R":
        run_quiz()
    else:
        clear_screen()
        print(f"{FG_NEON}Goodbye!{RESET}")


if __name__ == "__main__":
    try:
        run_quiz()
    except KeyboardInterrupt:
        print(f"\n{FG_GREY}Interrupted. Bye!{RESET}")
