"""
Tests for utility functions in the precision_truncator package.
"""

import pytest
from precision_truncator.utils import (
    count_tokens,
    split_into_sentences,
    extract_key_sentences,
    calculate_sentence_importance,
    extract_entities
)


def test_count_tokens():
    """Test token counting function."""
    text = "This is a simple test with seven words."
    assert count_tokens(text) == 7
    
    # Empty text
    assert count_tokens("") == 0
    
    # Text with multiple spaces
    assert count_tokens("This  has  double  spaces") == 4


def test_split_into_sentences():
    """Test sentence splitting function."""
    text = "This is one sentence. This is another! And a third? Let's go again."
    sentences = split_into_sentences(text)
    
    assert len(sentences) == 4
    assert sentences[0] == "This is one sentence."
    assert sentences[1] == "This is another!"
    assert sentences[2] == "And a third?"
    assert sentences[3] == "Let's go again."


def test_split_with_abbreviations():
    """Test sentence splitting with abbreviations."""
    text = "Mr. Smith went to Washington D.C. He met Dr. Johnson there."
    sentences = split_into_sentences(text)
    
    # Should be two sentences, not four
    assert len(sentences) == 2


def test_extract_key_sentences():
    """Test extraction of key sentences."""
    text = """
    This is a regular sentence. 
    This is an important conclusion to our research. 
    The sky is blue today. 
    We found that 75% of users preferred the new interface.
    """
    
    key_sentences = extract_key_sentences(text)
    
    # The important sentences should be earlier in the list
    important_sentence = "This is an important conclusion to our research."
    stats_sentence = "We found that 75% of users preferred the new interface."
    
    # Both important sentences should be present
    assert important_sentence in key_sentences
    assert stats_sentence in key_sentences
    
    # Empty text case
    assert extract_key_sentences("") == []


def test_calculate_sentence_importance():
    """Test calculation of sentence importance."""
    # Test sentence with importance indicators
    important = "This is an important conclusion to our findings."
    normal = "The sky is blue today."
    
    # Position-based importance (first and last sentences)
    first_pos_score = calculate_sentence_importance(normal, 0, 10)
    middle_pos_score = calculate_sentence_importance(normal, 5, 10)
    last_pos_score = calculate_sentence_importance(normal, 9, 10)
    
    # First and last should score higher than middle
    assert first_pos_score > middle_pos_score
    assert last_pos_score > middle_pos_score
    
    # Keyword-based importance
    important_score = calculate_sentence_importance(important, 5, 10)
    normal_score = calculate_sentence_importance(normal, 5, 10)
    
    # Sentence with "important" should score higher
    assert important_score > normal_score
    
    # Sentences with numbers should score higher
    numbers = "The research showed a 45% increase in performance."
    numbers_score = calculate_sentence_importance(numbers, 5, 10)
    assert numbers_score > normal_score


def test_extract_entities():
    """Test extraction of named entities."""
    text = "John Smith went to New York City to meet Jane Doe at IBM Headquarters."
    entities = extract_entities(text)
    
    # Should find these entities
    assert "John Smith" in entities
    assert "New York City" in entities
    assert "Jane Doe" in entities
    assert "IBM Headquarters" in entities
    
    # Empty text case
    assert extract_entities("") == {}
    
    # Text with no entities
    assert extract_entities("the cat sat on the mat") == {}