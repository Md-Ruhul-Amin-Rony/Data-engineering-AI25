# Lecture 1.3 — Bash hands-on 🖥️

Companion exercises for **Lecture 1.3 – Bash Intro** (Data Engineering, week 33).
Work through it top to bottom in a terminal. Type the commands — don't paste them.
Copy-paste teaches your clipboard, not you.

> **Where do I run this?**
> macOS/Linux: your normal terminal.
> Windows: WSL 2, or a GitHub Codespace in the browser (`Code ▸ Codespaces ▸ Create`)
> — a Codespace is a Linux box, so every command below works unchanged.

Files in this folder:

| File | What it is |
| --- | --- |
| `README.md` | this walkthrough |
| `movefiles.sh` | the lecture demo script (create/move/clean up) |

---

## 0. Where am I? 🧭

A shell session always has a *current directory*. Every relative path is
interpreted from there, which is why "it works on my machine" so often means
"I ran it from a different folder".

```bash
pwd                 # print working directory
ls -al              # everything, including dotfiles, with permissions
cd ..               # up one level (the parent)
cd -                # back to where I just was
cd                  # straight home
```

Set up a workspace for the whole lecture. Go home first, so it ends up
somewhere predictable regardless of where you were just poking around:

```bash
cd
mkdir -p de-lecture1/data/weather
cd de-lecture1
tree . 2>/dev/null || find . -type d
```

`mkdir -p` creates parents as needed **and** does not complain if the folder
already exists — that is exactly what you want inside a script.

---

## 1. Reading the manual (without an LLM) 📖

Your model of choice will be down, rate-limited, or not allowed on the exam.
The docs ship with the machine:

```bash
man ls              # q to quit, / to search
ls --help | head -20
tldr tar            # if installed: examples instead of prose
type -a ls          # is it a binary, an alias, or a shell builtin?
```

**Exercise 0.** Use `man ls` to find the flag that sorts by modification time,
and the one that prints human-readable file sizes. Combine them.

---

## 2. echo, dates and variables 🗓️

`echo` prints. It is also the fastest way to check what a variable actually
contains before a script eats it.

```bash
echo "Data engineering: 10% modelling, 90% wondering why the file is empty."
echo -e "line one\nline two"        # -e turns on escape sequences
```

Timestamps are the bread and butter of ingestion — every raw file you land
should say *when* it landed:

```bash
date                                 # local default format
date +%Y-%m-%d                       # 2026-08-11
date -u "+%Y-%m-%dT%H:%M:%SZ"        # UTC, ISO 8601 — use this in pipelines
```

Store it in a variable and reuse it:

```bash
STAMP=$(date -u +%Y%m%d_%H%M)
echo "Run started at $STAMP"
echo "Writing to data/weather/${STAMP}.json"
```

Two rules that will save you hours:

* Always `"$QUOTE"` your variables — otherwise a space in a filename becomes
  two arguments.
* `${STAMP}` braces let you glue a variable to text: `${STAMP}.json`.

---

## 3. Download and land some real data 💾

We will grab hourly temperature readings for Göteborg from SMHI’s open API and land it as
a timestamped raw file — the smallest possible version of an ingestion job.

```bash
cd ~/de-lecture1
STAMP=$(date -u +%Y%m%d_%H%M)
URL="https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/1/station/71420/period/latest-hour/data.json"

curl -sS -f "$URL" -o "data/weather/${STAMP}.json"
ls -lh data/weather/
```

* `-s` silent, `-S` but still show errors, `-f` fail loudly on HTTP 404/500
  instead of writing an HTML error page into your data lake.

Now look at it. Never trust a file you have not looked at:

```bash
cat data/weather/${STAMP}.json | head -c 300; echo
jq '.station.name, .value[0]' data/weather/${STAMP}.json   # if jq is installed
wc -c data/weather/${STAMP}.json
```

**Exercise 1.** Download the file twice, one minute apart. Confirm you got two
files, not one overwritten file. Why does the timestamp in the name matter?

---

## 4. Looking inside big files 🔍

You will meet CSVs too large for VS Code. The shell does not care about size.

```bash
printf 'id,city,pm25\n1,Göteborg,7\n2,Stockholm,9\n3,Malmö,12\n' > data/cities.csv

head -2 data/cities.csv        # first rows — check the header
tail -1 data/cities.csv        # last row — check the file is complete
wc -l data/cities.csv          # how many rows (header included!)
cut -d, -f2 data/cities.csv    # just the city column
grep -i malmo data/cities.csv || grep -i "Malmö" data/cities.csv
less data/cities.csv           # scroll, q to quit
```

---

## 5. Pipes and redirection 🔗

One tool, one job; the pipe glues them together.

```bash
ls data | wc -l                        # count entries
tail -n +2 data/cities.csv | sort -t, -k3 -nr | head -1   # highest pm25
echo "run ok $(date -u +%FT%TZ)" >> ingest.log            # append, don't clobber
curl -sS -f "$URL" | jq '.value[0].value' > data/latest_value.json  # no temp file needed
```

`>` overwrites, `>>` appends. Getting these two mixed up is a rite of passage;
do it here rather than in production.

---

## 6. Your first script 📂

A script is just the commands you already typed, saved so future-you does not
have to remember them.

```bash
touch init_repo.sh
nano init_repo.sh      # or: code init_repo.sh / vim init_repo.sh
```

Paste this in:

```bash
#!/bin/bash
set -euo pipefail      # stop on error, on unset variable, on failed pipe

echo "Initialising project layout…"
mkdir -p theory code-alongs explorations data/raw data/processed
touch theory/.gitkeep code-alongs/.gitkeep data/raw/.gitkeep

for i in {1..5}; do
    echo "notes for session $i" > "explorations/session$i.md"
done

echo "Done. Structure:"
ls -R . | head -30
```

The shebang `#!/bin/bash` tells the OS which interpreter to use.
`set -euo pipefail` is the single most valuable line in the file: without it a
failing command in the middle is silently ignored and the script "succeeds".

Run it:

```bash
./init_repo.sh
```

Permission denied ❌ — expected. Look at why, then fix it:

```bash
ls -al init_repo.sh     # -rw-r--r--  : no x, so nothing may execute it
chmod +x init_repo.sh   # add the execute bit
ls -al init_repo.sh     # -rwxr-xr-x
./init_repo.sh
```

(`bash init_repo.sh` also works and skips the `chmod` — you are handing the
file to an interpreter instead of asking the OS to execute it.)

Tidy up when you are done:

```bash
mv *.md explorations/ 2>/dev/null
rm -rf theory code-alongs explorations
```

`rm -rf` does not ask, does not use a trash can, and does not care how
important the folder was. Read the line twice before pressing Enter.

---

## 7. The script in this folder

You've been working in `~/de-lecture1` since section 0 — this script lives
back in the repo, not there. `cd` back first:

```bash
cd /workspaces/Data-engineering-AI25/lectures/code/Lecture1/lecture-1-bash
```

```bash
bash movefiles.sh      # the lecture demo: create, write, move, clean up
```

Open it in an editor first and predict what it will do — then run it and
check whether you were right.

---

## 8. Exercises ✅

Core repeats what `movefiles.sh` does — the point is doing it by hand, not
watching it. Then and Advanced revisit Sections 3–6 unaided, with new data,
building up to a script of your own.

**Core** — from the lecture:

1. Create a folder `folder1`.
2. Create two `.txt` files inside it, each with one line of text.
3. Navigate back out of the folder.
4. Create `folder2`.
5. Move the files from `folder1` to `folder2`.
6. Delete `folder1`.
7. Prove each step with `ls -al` / `pwd` before moving on.

**Then** — data-flavoured:

8. Land the SMHI file into `data/weather/` with a UTC timestamp in the name.
9. Count the lines of `data/cities.csv` *without* the header row.
10. Append one line per run to `ingest.log`, then show only the last 3 runs.
11. Find every `.md` file under your project: `find . -name "*.md"`.

**Advanced** — scripting:

12. Write `ingest.sh` that: makes `data/raw/` if missing, downloads the SMHI
    JSON to a timestamped file, logs success or failure to `ingest.log`, and
    exits non-zero if the download fails. Start with `set -euo pipefail`.
13. Make it executable with `chmod +x` and run it via `./ingest.sh`.
14. Loop over the files in `data/raw/` and print name + size for each.
15. Bonus: add `--dry-run` handling, so `./ingest.sh --dry-run` only prints the
    commands it *would* run.

---

## 9. Survival kit 🧰

| Keys / command | Why you care |
| --- | --- |
| `Tab` | complete paths; also tells you when a path is wrong |
| `Ctrl+R` | search your command history — you type the good ones once |
| `Ctrl+C` / `Ctrl+D` | stop a running command / end input |
| `↑` | the most-used key in data engineering |
| `history \| grep curl` | what did I actually run an hour ago? |
| `man` / `--help` / `tldr` | documentation that works offline |
| `set -euo pipefail` | scripts that fail loudly instead of quietly |

## Resources

* [The Missing Semester of Your CS Education (MIT)](https://missing.csail.mit.edu/) — lectures 1–3
* [ExplainShell](https://explainshell.com/) — paste a command, get every flag explained
* [ShellCheck](https://www.shellcheck.net/) — linter for your scripts
* `man bash` — when you want the whole truth
