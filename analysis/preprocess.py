"""Text preprocessing utilities for Lewis Carroll works."""

import re
from typing import List, Tuple


def strip_gutenberg_headers(text: str) -> str:
    """Remove Project Gutenberg headers and footers."""
    # Find start marker
    start_patterns = [
        r'\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK .+ \*\*\*',
        r'START OF THE PROJECT GUTENBERG EBOOK',
    ]

    # Find end marker
    end_patterns = [
        r'\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK .+ \*\*\*',
        r'END OF THE PROJECT GUTENBERG EBOOK',
    ]

    # Try to find and remove header
    for pattern in start_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            text = text[match.end():]
            break

    # Try to find and remove footer
    for pattern in end_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            text = text[:match.start()]
            break

    return text.strip()


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep sentence punctuation
    text = re.sub(r'[^\w\s.!?,;:\'\"-]', '', text)
    return text.strip()


def tokenize_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    # Simple sentence tokenization
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]


def tokenize_words(text: str) -> List[str]:
    """Split text into words."""
    # Remove punctuation and split
    text = re.sub(r'[^\w\s]', '', text)
    words = text.lower().split()
    return [w for w in words if w]


def preprocess_file(filepath: str) -> Tuple[str, str, List[str], List[str]]:
    """
    Preprocess a text file.

    Returns:
        (raw_text, cleaned_text, sentences, words)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Strip Gutenberg metadata
    text = strip_gutenberg_headers(raw_text)

    # Clean text
    cleaned_text = clean_text(text)

    # Tokenize
    sentences = tokenize_sentences(cleaned_text)
    words = tokenize_words(cleaned_text)

    return raw_text, cleaned_text, sentences, words
