"""NLP processing module for job description analysis and keyword extraction."""

from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Standard fallback stopwords in case NLTK corpus cannot be fetched offline
FALLBACK_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}

# Ensure necessary NLTK datasets are downloaded safely
for res in ["punkt", "punkt_tab", "stopwords"]:
    try:
        nltk.download(res, quiet=True)
    except Exception:
        pass


def preprocess_text(text: str) -> list:
    """Preprocess text by tokenizing, converting to lowercase, and removing stop words.

    Concepts explained:
    - Tokenization: Splitting a continuous body of text into individual units (tokens/words).
    - Stop-word removal: Filtering out frequent grammatical words (e.g., 'and', 'the', 'is')
      that don't carry domain-specific meaning.
    - Punctuation removal: Eliminating punctuation marks and non-alphabetic symbols.
    """
    if not text or not isinstance(text, str):
        return []

    # 1. Lowercasing: Normalize text so 'Python' and 'python' are treated as identical
    text_lower = text.lower()

    # 2. Tokenization: Break sentences into individual word tokens using NLTK (with regex fallback)
    try:
        tokens = word_tokenize(text_lower)
    except Exception:
        tokens = re.findall(r"\b[a-zA-Z]+\b", text_lower)

    # 3. Stop words setup: Standard English stop words with fallback
    try:
        stop_words = set(stopwords.words("english"))
    except Exception:
        stop_words = FALLBACK_STOPWORDS

    # 4. Filter tokens: Keep only alphabetic tokens that are not stop words
    cleaned_tokens = [
        token for token in tokens
        if token.isalpha() and token not in stop_words
    ]

    return cleaned_tokens


def extract_keywords(text: str, top_n: int = 15) -> list:
    """Extract the most frequent useful keywords from the given text.

    Concepts explained:
    - Keyword extraction: Identifying the most prominent terms in a job description.
    - Length filtering: Words with fewer than 3 characters are filtered out.
    - Frequency counting: High frequency of relevant terms indicates key job skills/responsibilities.
    """
    if not text or not isinstance(text, str):
        return []

    # Preprocess the text into clean tokens
    tokens = preprocess_text(text)

    # Filter out very short words with fewer than 3 characters
    useful_words = [token for token in tokens if len(token) >= 3]

    if not useful_words:
        return []

    # Count frequency of each word
    word_counts = Counter(useful_words)

    # Extract the most frequent keywords as a list of words
    most_common_keywords = [word for word, _ in word_counts.most_common(top_n)]

    return most_common_keywords
