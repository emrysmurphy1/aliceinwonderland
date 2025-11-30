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


def calculate_advanced_metrics(text: str, cleaned_text: str) -> Dict[str, Any]:
    """Calculate advanced literary metrics."""
    import re

    # Punctuation patterns
    exclamations = len(re.findall(r'!', text))
    questions = len(re.findall(r'\?', text))
    dashes = len(re.findall(r'—|--', text))

    # Dialogue detection (text in quotes)
    dialogue_matches = re.findall(r'"[^"]*"', text)
    dialogue_words = sum(len(d.split()) for d in dialogue_matches)
    total_words_raw = len(text.split())
    dialogue_ratio = (dialogue_words / total_words_raw * 100) if total_words_raw > 0 else 0

    # Sentence length variation (standard deviation)
    sentences = re.split(r'[.!?]+', cleaned_text)
    sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
    if sentence_lengths:
        avg_len = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((l - avg_len) ** 2 for l in sentence_lengths) / len(sentence_lengths)
        std_dev = variance ** 0.5
    else:
        std_dev = 0

    # Common repeated phrases (2-3 words)
    words = cleaned_text.lower().split()
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    trigrams = [f"{words[i]} {words[i+1]} {words[i+2]}" for i in range(len(words)-2)]

    common_bigrams = Counter(bigrams).most_common(10)
    common_trigrams = Counter(trigrams).most_common(5)

    return {
        'exclamations': exclamations,
        'questions': questions,
        'dashes': dashes,
        'dialogue_percentage': round(dialogue_ratio, 2),
        'sentence_length_variation': round(std_dev, 2),
        'common_phrases': {
            'bigrams': dict(common_bigrams),
            'trigrams': dict(common_trigrams)
        }
    }


def calculate_style_metrics(text: str, sentences: List[str], words: List[str]) -> Dict[str, Any]:
    """Calculate various style metrics."""
    total_words = len(words)
    unique_words = len(set(words))
    total_sentences = len(sentences)

    # Calculate metrics
    avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0
    avg_word_length = sum(len(w) for w in words) / total_words if total_words > 0 else 0
    lexical_diversity = unique_words / total_words if total_words > 0 else 0

    # Word length distribution
    word_lengths = [len(w) for w in words]
    short_words = sum(1 for l in word_lengths if l <= 4)
    medium_words = sum(1 for l in word_lengths if 5 <= l <= 7)
    long_words = sum(1 for l in word_lengths if l > 7)

    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'total_sentences': total_sentences,
        'avg_sentence_length': round(avg_sentence_length, 2),
        'avg_word_length': round(avg_word_length, 2),
        'lexical_diversity': round(lexical_diversity, 4),
        'vocabulary_richness': round(lexical_diversity * 100, 2),
        'word_length_dist': {
            'short': round(short_words / total_words * 100, 1) if total_words > 0 else 0,
            'medium': round(medium_words / total_words * 100, 1) if total_words > 0 else 0,
            'long': round(long_words / total_words * 100, 1) if total_words > 0 else 0
        }
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
    advanced_metrics = calculate_advanced_metrics(raw_text, cleaned_text)

    return {
        'id': metadata['id'],
        'title': metadata['title'],
        'short_title': metadata['short_title'],
        'sentiment': sentiment,
        'word_frequencies': bag_of_words,
        'style': style_metrics,
        'advanced': advanced_metrics
    }


def generate_comparison_data(analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate comparison data across all books."""
    comparison = {
        'sentiment_comparison': {},
        'style_comparison': {},
        'advanced_comparison': {},
        'vocabulary_analysis': {}
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

    # Compare advanced metrics
    for analysis in analyses:
        book_id = analysis['id']
        comparison['advanced_comparison'][book_id] = {
            'title': analysis['short_title'],
            **{k: v for k, v in analysis['advanced'].items() if k != 'common_phrases'}
        }

    # Vocabulary analysis
    all_word_sets = {analysis['id']: set(analysis['word_frequencies'].keys())
                     for analysis in analyses}

    # Find common words across all books
    common_words = set.intersection(*all_word_sets.values()) if all_word_sets else set()

    # Find unique words per book (words that appear in only one book)
    unique_per_book = {}
    for book_id, words in all_word_sets.items():
        other_words = set()
        for other_id, other_word_set in all_word_sets.items():
            if other_id != book_id:
                other_words.update(other_word_set)
        unique_words = words - other_words
        unique_per_book[book_id] = len(unique_words)

    # Calculate overlap percentages
    overlap_matrix = {}
    for id1, words1 in all_word_sets.items():
        overlap_matrix[id1] = {}
        for id2, words2 in all_word_sets.items():
            if id1 != id2:
                overlap = len(words1 & words2)
                overlap_pct = (overlap / len(words1) * 100) if len(words1) > 0 else 0
                overlap_matrix[id1][id2] = round(overlap_pct, 1)

    comparison['vocabulary_analysis'] = {
        'common_words_count': len(common_words),
        'common_words': list(common_words)[:20],  # Top 20 common words
        'unique_words_per_book': unique_per_book,
        'overlap_matrix': overlap_matrix
    }

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
