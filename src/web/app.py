from flask import Flask, render_template, request
import os
from src.pipeline.downloader import download_audio
from src.pipeline.transcriber import transcribe_audio
from src.pipeline.summarizer import summarize_text


app = Flask(__name__, template_folder="templates")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
TRANSCRIPT_DIR = os.path.join(OUTPUT_DIR, "transcripts")
SUMMARY_DIR = os.path.join(OUTPUT_DIR, "summaries")

for d in [OUTPUT_DIR, AUDIO_DIR, TRANSCRIPT_DIR, SUMMARY_DIR]:
    os.makedirs(d, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    transcript = ""
    error = ""

    if request.method == "POST":
        url = request.form.get("youtube_url")

        if not url or "youtube.com" not in url and "youtu.be" not in url:
            error = "Invalid YouTube URL"
            return render_template("index.html", error=error)

        try:
            audio_path = download_audio(url, AUDIO_DIR)
            transcript = transcribe_audio(audio_path, TRANSCRIPT_DIR)
            summary = summarize_text(transcript)

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
