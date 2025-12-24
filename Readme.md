# Offline YouTube Video Summarizer

## 1. Project Overview

This project is an **Offline YouTube Video Summarizer** that automatically generates a text summary from a YouTube video.
The system works entirely **offline after the initial model download** and follows an end-to-end pipeline:

1. Download audio from a YouTube video
2. Convert speech to text using a speech-to-text model
3. Summarize the transcript using NLP techniques
4. Display both the transcript and summary through a web interface

The goal of the project is to demonstrate the practical integration of **speech recognition**, **natural language processing**, and **web application development**, while remaining compatible with **consumer-grade hardware**.

---

## 2. Setup and Installation Instructions

### 2.1 Prerequisites

* **Operating System:** Windows
* **Python:** 3.11.x
* **GPU (optional but recommended):** NVIDIA GPU with CUDA support
* **FFmpeg:** Required for audio processing

---

### 2.2 Clone the Repository

```bash
git clone <repository-url>
cd offline-youtube-summarizer
```

---

### 2.3 Create and Activate Virtual Environment

```bash
py -3.11 -m venv venv311
venv311\Scripts\activate
```

---

### 2.4 Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 2.5 Install PyTorch with CUDA Support (Recommended)

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

This enables GPU acceleration for transcription and summarization.

---

### 2.6 Install FFmpeg

1. Download FFmpeg from: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract it to any folder (e.g., `C:\ffmpeg`)
3. Add the `bin` folder to your system **PATH**

Verify installation:

```bash
ffmpeg -version
```

---

### 2.7 Model Downloads (Automatic)

The following models are downloaded automatically on first run:

* Whisper (via faster-whisper)
* BART-large-CNN (via Hugging Face)

Once downloaded, the application works **offline**.

---

### 2.8 Run the Application

```bash
python -m app.app
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 3. Design Choices and Justification

### 3.1 Audio Download – yt-dlp

* Chosen for reliable YouTube audio extraction
* Actively maintained and supports multiple formats
* Works seamlessly with FFmpeg

**Trade-off:** Requires FFmpeg installation, but ensures high-quality audio.

---

### 3.2 Transcription – Whisper (faster-whisper)

* Provides accurate speech-to-text conversion
* Faster-whisper was chosen for:

  * Lower memory usage
  * Faster inference
  * Compatibility with consumer GPUs

**Trade-off:** Smaller Whisper models are faster but slightly less accurate than larger ones.

---

### 3.3 Summarization – BART-large-CNN

* Specifically trained for abstractive summarization
* Produces more coherent and structured summaries than lightweight models

**Model evolution:**

* Original GitHub model: `distilbart-cnn-12-6`
* First replacement: `t5-small` (lighter but weak summaries)
* Final model: `facebook/bart-large-cnn`

**Trade-off:** Higher memory usage, mitigated using chunk-based processing.

---

### 3.4 Chunking and Hierarchical Processing

* Long transcripts exceed transformer token limits
* Text is split into manageable chunks
* Each chunk is summarized independently (one-pass method)

**Benefit:** Prevents memory overflow and maintains performance on long videos.

---

### 3.5 Web Framework – Flask

* Lightweight and easy to integrate with ML pipelines
* Handles routing, form submission, and rendering results

**Trade-off:** Not designed for high-scale production, but ideal for academic projects.

---

## 4. Usage

### 4.1 Using the Web Interface

1. Start the Flask server
2. Open the browser at `http://127.0.0.1:5000`
3. Paste a valid YouTube video URL
4. Click **Generate Summary**
5. View:

   * Full transcript
   * Generated summary

---

### 4.2 Output Files

Generated files are stored in the `outputs/` directory:

* Downloaded audio
* Transcript text

---

## 5. Challenges Faced

### 5.1 Model Selection Issues

* The original summarization model from the GitHub repository produced weak results on long transcripts.
* Switching to a lighter model (`t5-small`) improved stability but reduced summary quality.

**Solution:** Adopted BART-large-CNN with chunking to balance quality and feasibility.

---

### 5.2 Summarization Quality on Speeches

* Abstractive models tended to paraphrase motivational speeches instead of compressing them.

**Solution:** Explored one-pass summarization and extractive approaches for better factual compression.

---

### 5.3 Hardware Constraints

* Limited GPU memory (4 GB VRAM) restricted model size.

**Solution:** Used optimized models, chunking, and careful parameter tuning.

---

### 5.4 Dependency and Environment Issues

* CUDA, cuDNN, and Python version mismatches caused installation errors.

**Solution:** Standardized on Python 3.11 and PyTorch CUDA 12.1 wheels.

---

### 5.5 Handling Long Videos

* Long videos exceed model context limits and system memory.

**Solution:**
Implemented audio chunking to split long inputs into manageable segments, followed by transcript aggregation before summarization.
