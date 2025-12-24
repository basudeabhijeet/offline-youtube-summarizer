from transformers import pipeline
import torch

# Load BART summarization model
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=0 if torch.cuda.is_available() else -1
)


def chunk_text(text, max_words=300):
    """
    Split text into manageable chunks for BART
    """
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])


def summarize_text(text):
    """
    ONE-PASS summarization using BART
    (chunk → summary → concatenate)
    """

    chunk_summaries = []

    for chunk in chunk_text(text):
        result = summarizer(
            chunk,
            max_length=130,
            min_length=60,
            do_sample=False,
            num_beams=4,
            repetition_penalty=2.0,
            length_penalty=1.0,
            truncation=True
        )
        chunk_summaries.append(result[0]["summary_text"])

    # Directly return combined summaries (NO second pass)
    return " ".join(chunk_summaries)
