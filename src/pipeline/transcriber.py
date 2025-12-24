from faster_whisper import WhisperModel
import os

# GPU-enabled Whisper (safe for GTX 1650)
model = WhisperModel(
    "small",
    device="cuda",
    compute_type="float16"
)

def transcribe_audio(audio_path, output_dir):
    segments, _ = model.transcribe(audio_path)

    transcript = ""
    for segment in segments:
        transcript += segment.text.strip() + " "

    filename = os.path.basename(audio_path).replace(".wav", ".txt")
    out_path = os.path.join(output_dir, filename)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    return transcript
