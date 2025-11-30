#!/usr/bin/env python3
"""Analyze Lewis Carroll texts and generate JSON output."""

import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Any

import nltk
from textblob import TextBlob
from preprocess import preprocess_file

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords

# Book metadata
BOOKS = {
    'pg19033.txt': {
        'title': "Alice's Adventures in Wonderland",
        'short_title': 'Alice in Wonderland',
        'id': 'alice'
    },
    'pg651.txt': {
        'title': 'Phantasmagoria and Other Poems',
        'short_title': 'Phantasmagoria',
        'id': 'phantasmagoria'
    },
    'pg33582.txt': {
        'title': 'Rhyme? and Reason?',
        'short_title': 'Rhyme and Reason',
        'id': 'rhyme'
    },
    'pg35535.txt': {
        'title': 'Feeding the Mind',
        'short_title': 'Feeding the Mind',
        'id': 'feeding'
    }
}


def get_sentiment(text: str) -> Dict[str, float]:
    """Analyze sentiment using TextBlob."""
    blob = TextBlob(text)
    return {
        'polarity': round(blob.sentiment.polarity, 3),  # -1 to 1
        'subjectivity': round(blob.sentiment.subjectivity, 3)  # 0 to 1
    }


def get_bag_of_words(words: List[str], top_n: int = 100) -> Dict[str, int]:
    """Create bag of words with stopwords removed."""
    stop_words = set(stopwords.words('english'))
    # Filter out stopwords and very short words
    filtered_words = [w for w in words if w not in stop_words and len(w) > 2]

    # Count frequencies
    word_counts = Counter(filtered_words)
    return dict(word_counts.most_common(top_n))


def calculate_style_metrics(text: str, sentences: List[str], words: List[str]) -> Dict[str, Any]:
    """Calculate various style metrics."""
    total_words = len(words)
    unique_words = len(set(words))
    total_sentences = len(sentences)

    # Calculate metrics
    avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0
    avg_word_length = sum(len(w) for w in words) / total_words if total_words > 0 else 0
    lexical_diversity = unique_words / total_words if total_words > 0 else 0

    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'total_sentences': total_sentences,
        'avg_sentence_length': round(avg_sentence_length, 2),
        'avg_word_length': round(avg_word_length, 2),
        'lexical_diversity': round(lexical_diversity, 4),
        'vocabulary_richness': round(lexical_diversity * 100, 2)  # As percentage
    }


def analyze_book(filepath: str, metadata: Dict[str, str]) -> Dict[str, Any]:
    """Analyze a single book."""
    print(f"Analyzing {metadata['title']}...")

    # Preprocess
    raw_text, cleaned_text, sentences, words = preprocess_file(filepath)

    # Perform analyses
    sentiment = get_sentiment(cleaned_text)
    bag_of_words = get_bag_of_words(words, top_n=100)
    style_metrics = calculate_style_metrics(cleaned_text, sentences, words)

    return {
        'id': metadata['id'],
        'title': metadata['title'],
        'short_title': metadata['short_title'],
        'sentiment': sentiment,
        'word_frequencies': bag_of_words,
        'style': style_metrics
    }


def generate_comparison_data(analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate comparison data across all books."""
    comparison = {
        'sentiment_comparison': {},
        'style_comparison': {},
        'word_overlap': {}
    }

    # Compare sentiments
    for analysis in analyses:
        book_id = analysis['id']
        comparison['sentiment_comparison'][book_id] = {
            'title': analysis['short_title'],
            'polarity': analysis['sentiment']['polarity'],
            'subjectivity': analysis['sentiment']['subjectivity']
        }

    # Compare style metrics
    for analysis in analyses:
        book_id = analysis['id']
        comparison['style_comparison'][book_id] = {
            'title': analysis['short_title'],
            **analysis['style']
        }

    # Find common words across books
    all_words = [set(analysis['word_frequencies'].keys()) for analysis in analyses]
    common_words = set.intersection(*all_words) if all_words else set()
    comparison['common_top_words'] = list(common_words)

    return comparison


def main():
    """Main analysis pipeline."""
    # Setup paths
    tests_dir = Path(__file__).parent.parent / 'tests'
    output_dir = Path(__file__).parent.parent / 'docs' / 'data'
    output_file = output_dir / 'analysis.json'

    # Analyze all books
    analyses = []
    for filename, metadata in BOOKS.items():
        filepath = tests_dir / filename
        if not filepath.exists():
            print(f"Warning: {filename} not found, skipping...")
            continue

        analysis = analyze_book(str(filepath), metadata)
        analyses.append(analysis)

    # Generate comparison data
    comparison = generate_comparison_data(analyses)

    # Combine all data
    output_data = {
        'books': analyses,
        'comparison': comparison,
        'metadata': {
            'total_books': len(analyses),
            'analysis_version': '1.0'
        }
    }

    # Save to JSON
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Analysis complete! Output saved to {output_file}")
    print(f"  Analyzed {len(analyses)} books")
    print(f"  Total unique words across all books: {sum(a['style']['unique_words'] for a in analyses)}")


if __name__ == '__main__':
    main()
