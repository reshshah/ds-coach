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
INPUT_DIR = "input"
OUTPUT_DIR = "output"
AUDIO_FILE = os.path.join(INPUT_DIR, "reel_audio.mp3")
ALL_SUMMARIES_FILE = os.path.join(OUTPUT_DIR, "all_summaries.txt")
# ─────────────────────────────────────────────────────────────


def ensure_dirs():
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def download_audio(url):
    print(f"\n[1/4] Downloading audio from URL...")
    if os.path.exists(AUDIO_FILE):
        os.remove(AUDIO_FILE)
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
    answer = input(f"    Open {os.path.basename(filename)} in VSCode? [Y/n]: ").strip().lower()
    if answer in ("", "y", "yes"):
        subprocess.run(["code", filename])


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
    ensure_dirs()

    print("=" * 60)
    print("  Reel Transcriber + Summarizer")
    print("=" * 60)

    url = input("\nPaste the Instagram Reel URL: ").strip()
    if not url:
        print("No URL entered. Exiting.")
        return

    video_name = input("Enter a name for this video (e.g. 'hyperparameters explained'): ").strip()
    if not video_name:
        video_name = "untitled"

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    slug = video_name.lower().replace(" ", "_")[:40]
    filename_base = f"{date_str[:10]}_{slug}"
    transcript_file = os.path.join(OUTPUT_DIR, f"{filename_base}_transcript.txt")
    summary_file = os.path.join(OUTPUT_DIR, f"{filename_base}_summary.txt")

    if not download_audio(url):
        return

    transcript = transcribe(AUDIO_FILE)
    save(transcript, transcript_file)

    print(f"\n--- TRANSCRIPT PREVIEW ---")
    print(transcript[:300] + ("..." if len(transcript) > 300 else ""))

    summary = summarize(transcript)
    save(summary, summary_file)

    print(f"\n--- SUMMARY ---")
    print(summary)

    append_to_master(video_name, url, date_str, transcript, summary)

    print(f"\nFiles saved:")
    print(f"  {transcript_file}")
    print(f"  {summary_file}")
    print(f"  {ALL_SUMMARIES_FILE}  (all videos appended here)")
    print("\nDone.")


if __name__ == "__main__":
    main()
