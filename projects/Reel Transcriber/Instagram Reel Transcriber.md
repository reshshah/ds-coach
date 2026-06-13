# Instagram Reel Transcriber — Complete Setup Guide
Transcribe any Instagram Reel to text and summarize it locally using Whisper + Ollama + Llama 3. No API keys. No cost. Runs fully on your Mac.

---

## What You Need (One-Time Setup)

- Mac with Python 3 installed
- VSCode installed (code.visualstudio.com)
- Internet connection for downloads (everything runs offline after)

---

## One-Time Setup

### 1. Create Your Project Folder
- Open VSCode
- `File` → `Open Folder` → create a new folder called `Reel Transcriber`

### 2. Open Terminal in VSCode
Press `` Ctrl + ` `` (backtick)

### 3. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```
You'll see `(venv)` at the start of your terminal line. This means it's active.

### 4. Install ffmpeg
```bash
brew install ffmpeg
```

### 5. Install Python Packages
```bash
python3 -m pip install yt-dlp openai-whisper transformers torch
```

### 6. Install Ollama
Do NOT use Homebrew for Ollama — the Homebrew version is missing required binaries.

Download the official Mac app instead:
- Go to ollama.com → Download for Mac
- Open the `.dmg` → drag Ollama to Applications → open it once
- You'll see the Ollama icon in your Mac menu bar (top right)

### 7. Download Llama 3 Model (~4.7GB, downloads once)
```bash
ollama pull llama3:latest
```

## When you move this project to a new folder, run this so that all the required packages run in the venv of that folder:
rm -rf venv
python3 -m venv venv
source venv/bin/activate
python3 -m pip install yt-dlp openai-whisper transformers torch

---

## Create the Script

In VSCode left sidebar → click the `New File` icon → name it `transcribe.py`

Paste this:

```python
import warnings
warnings.filterwarnings("ignore")

import whisper
import os
import urllib.request
import json
import subprocess
from datetime import datetime

# ── CONFIG ───────────────────────────────────────────────────
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium
OLLAMA_MODEL = "llama3:latest"
AUDIO_FILE = "reel_audio.mp3"
ALL_SUMMARIES_FILE = "all_summaries.txt"
# ─────────────────────────────────────────────────────────────


def download_audio(url):
    print(f"\n[1/4] Downloading audio from URL...")
    result = subprocess.run(
        ["yt-dlp", "-x", "--audio-format", "mp3", url, "-o", AUDIO_FILE],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR downloading audio:\n{result.stderr}")
        return False
    print(f"    Saved → {AUDIO_FILE}")
    return True


def transcribe(audio_file):
    print(f"\n[2/4] Loading Whisper model ({WHISPER_MODEL})...")
    model = whisper.load_model(WHISPER_MODEL)
    print(f"[3/4] Transcribing {audio_file}...")
    result = model.transcribe(audio_file)
    return result["text"].strip()


def summarize(transcript):
    print("[4/4] Summarizing with Ollama + Llama 3 (running locally)...")

    prompt = f"""Summarize the following transcript from an Instagram Reel.

Make it:
- Easy to read in under 30 seconds
- Start with a 1-line TL;DR
- Followed by 3-5 key points in plain English
- End with 1 line on who this is useful for

Transcript:
{transcript}"""

    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")

    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data["response"].strip()


def save(text, filename):
    with open(filename, "w") as f:
        f.write(text)
    print(f"    Saved → {filename}")


def append_to_master(video_name, url, date_str, transcript, summary):
    with open(ALL_SUMMARIES_FILE, "a") as f:
        f.write("=" * 60 + "\n")
        f.write(f"VIDEO : {video_name}\n")
        f.write(f"URL   : {url}\n")
        f.write(f"DATE  : {date_str}\n")
        f.write("=" * 60 + "\n\n")
        f.write("--- SUMMARY ---\n")
        f.write(summary + "\n\n")
        f.write("--- FULL TRANSCRIPT ---\n")
        f.write(transcript + "\n\n")
    print(f"    Appended → {ALL_SUMMARIES_FILE}")


def main():
    print("=" * 60)
    print("  Reel Transcriber + Summarizer")
    print("=" * 60)

    # Ask for URL and video name
    url = input("\nPaste the Instagram Reel URL: ").strip()
    if not url:
        print("No URL entered. Exiting.")
        return

    video_name = input("Enter a name for this video (e.g. 'hyperparameters explained'): ").strip()
    if not video_name:
        video_name = "untitled"

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Build safe filename slug
    slug = video_name.lower().replace(" ", "_")[:40]
    filename_base = f"{date_str[:10]}_{slug}"
    transcript_file = f"{filename_base}_transcript.txt"
    summary_file = f"{filename_base}_summary.txt"

    # Download
    if not download_audio(url):
        return

    # Transcribe
    transcript = transcribe(AUDIO_FILE)
    save(transcript, transcript_file)

    print(f"\n--- TRANSCRIPT PREVIEW ---")
    print(transcript[:300] + ("..." if len(transcript) > 300 else ""))

    # Summarize
    summary = summarize(transcript)
    save(summary, summary_file)

    print(f"\n--- SUMMARY ---")
    print(summary)

    # Append to master log
    append_to_master(video_name, url, date_str, transcript, summary)

    print(f"\nFiles saved:")
    print(f"  {transcript_file}")
    print(f"  {summary_file}")
    print(f"  {ALL_SUMMARIES_FILE}  (all videos appended here)")
    print("\nDone.")


if __name__ == "__main__":
    main()
```

---

## Every Time You Use It

### Step 1: Open VSCode and activate your environment
```bash
source venv/bin/activate
```

### Step 2: Make sure Ollama is running
Check for the Ollama icon in your Mac menu bar. If not visible, open Ollama from Applications.

Optionally start it from terminal:
```bash
ollama serve
```

### Step 3: Run the script
```bash
python3 transcribe.py
```

The script will ask you:
```
Paste the Instagram Reel URL:
Enter a name for this video:
```

It handles download, transcription, and summarization automatically.

### Step 4: Read your output
- `YYYY-MM-DD_videoname_transcript.txt` — full word-for-word transcription
- `YYYY-MM-DD_videoname_summary.txt` — clean, organized summary from Llama 3
- `all_summaries.txt` — every video you've ever processed, appended here

---

## Your Output Files

| File | What's in it |
|---|---|
| `reel_audio.mp3` | Downloaded audio (overwritten each run) |
| `YYYY-MM-DD_name_transcript.txt` | Full transcription for that video |
| `YYYY-MM-DD_name_summary.txt` | TL;DR + key points for that video |
| `all_summaries.txt` | Master log — all videos, dates, URLs, summaries |

---

## Troubleshooting

| Error | Fix |
|---|---|
| `zsh: command not found: pip` | Use `python3 -m pip install ...` |
| `externally-managed-environment` | Create venv first: `python3 -m venv venv` |
| `(venv)` not showing | Run `source venv/bin/activate` |
| `ffprobe and ffmpeg not found` | Run `brew install ffmpeg` |
| `zsh: command not found: ollama` | Install the Mac app from ollama.com (not Homebrew) |
| `llama-server binary not found` | Uninstall Homebrew ollama, use the Mac app instead |
| `HTTP Error 500` on summarize | Run `ollama run llama3:latest "hi"` to test; model may not be loaded |
| `HTTP Error 404` on summarize | Model name wrong — run `ollama list` and update OLLAMA_MODEL in script |
| `Connection refused` on summarize | Ollama isn't running — open the app from Applications |
| FP16 warning from Whisper | Safe to ignore — cosmetic only |
| First transcription is slow | Whisper downloads model once (~140MB) — normal |
| First summarization is slow | Llama 3 loads into memory — normal, faster after |
| Moved the project folder | Delete venv and recreate: `rm -rf venv` then repeat Step 3 |

---

## How It Works

```
You paste Instagram Reel URL
           ↓
     yt-dlp (download audio)
           ↓
      reel_audio.mp3
           ↓
  Whisper (transcribe locally)
           ↓
  YYYY-MM-DD_name_transcript.txt
           ↓
  Ollama + Llama 3 (summarize locally)
           ↓
  YYYY-MM-DD_name_summary.txt
           +
     all_summaries.txt (master log)
```

---

## Notes
- Everything runs on your Mac — no API keys, no cost, no data sent anywhere
- Works on any public Instagram Reel
- For private Reels, add `--cookies-from-browser chrome` to the yt-dlp command inside `download_audio()`
- To improve transcription accuracy, change `WHISPER_MODEL = "base"` to `"small"` or `"medium"`
- Use the official Ollama Mac app — the Homebrew version is missing required binaries
