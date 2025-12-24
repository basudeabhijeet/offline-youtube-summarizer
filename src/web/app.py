from flask import Flask, render_template, request
import os

from src.pipeline.downloader import download_audio
from src.pipeline.transcriber import transcribe_audio
from src.pipeline.summarizer import summarize_text

app = Flask(__name__, template_folder="templates")

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
TRANSCRIPT_DIR = os.path.join(OUTPUT_DIR, "transcripts")
SUMMARY_DIR = os.path.join(OUTPUT_DIR, "summaries")

# Ensure directories exist
for d in [OUTPUT_DIR, AUDIO_DIR, TRANSCRIPT_DIR, SUMMARY_DIR]:
    os.makedirs(d, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    transcript = ""
    error = ""

    if request.method == "POST":
        url = request.form.get("youtube_url")

        if not url or ("youtube.com" not in url and "youtu.be" not in url):
            error = "Invalid YouTube URL"
            return render_template("index.html", error=error)

        try:
            # 1. Download audio
            audio_path = download_audio(url, AUDIO_DIR)

            # 2. Transcribe audio
            transcript = transcribe_audio(audio_path, TRANSCRIPT_DIR)

            # 3. Summarize transcript
            summary = summarize_text(transcript)

            # 4. SAVE SUMMARY TO FILE (FIX)
            video_id = os.path.splitext(os.path.basename(audio_path))[0]
            summary_path = os.path.join(SUMMARY_DIR, f"{video_id}_summary.txt")

            with open(summary_path, "w", encoding="utf-8") as f:
                f.write(summary)

        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template(
        "index.html",
        summary=summary,
        transcript=transcript,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
