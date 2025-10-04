from transformers import pipeline

# Lazy initialization - only load when needed
_summarizer = None

def _get_summarizer():
    global _summarizer
    if _summarizer is None:
        try:
            _summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        except Exception as e:
            print(f"Warning: Could not load summarizer model: {e}")
            _summarizer = False  # Mark as failed to avoid retrying
    return _summarizer if _summarizer is not False else None

def summarize(text):
    if not text:
        return ""
    summarizer = _get_summarizer()
    if summarizer is None:
        # Fallback: return first 100 words if model not available
        words = text.split()
        return " ".join(words[:30]) + ("..." if len(words) > 30 else "")
    result = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return result[0]['summary_text'] if result else ""