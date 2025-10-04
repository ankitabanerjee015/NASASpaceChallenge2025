from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize(text):
    if not text:
        return ""
    result = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return result[0]['summary_text'] if result else ""