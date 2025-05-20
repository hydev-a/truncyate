"""
Tests for the PrecisionTruncator class.
"""

import pytest
from precision_truncator import PrecisionTruncator, TruncationStrategy


@pytest.fixture
def sample_text():
    return """
    Artificial intelligence (AI) is intelligence demonstrated by machines, 
    as opposed to intelligence displayed by animals and humans. AI research 
    has been defined as the field of study of intelligent agents, which refers 
    to any system that perceives its environment and takes actions that 
    maximize its chance of achieving its goals.

    The term "artificial intelligence" had previously been used to describe 
    machines that mimic and display human cognitive skills that are associated 
    with the human mind, such as learning and problem-solving. This definition 
    has since been rejected by major AI researchers who now describe AI in 
    terms of rationality and acting rationally, which does not limit how 
    intelligence can be articulated.
    """


def test_init_requires_limit():
    """Test that initialization requires either max_tokens or max_chars."""
    with pytest.raises(ValueError):
        PrecisionTruncator()


def test_truncate_start_tokens(sample_text):
    """Test truncation from the start with token limit."""
    truncator = PrecisionTruncator(max_tokens=20)
    result = truncator.truncate(sample_text, TruncationStrategy.START)
    
    # Check if result is shorter than original
    assert len(result.split()) <= 20
    
    # Check that it starts with the beginning of the original text
    assert sample_text.strip().startswith(result.strip())


def test_truncate_end_tokens(sample_text):
    """Test truncation from the end with token limit."""
    truncator = PrecisionTruncator(max_tokens=20)
    result = truncator.truncate(sample_text, TruncationStrategy.END)
    
    # Check if result is shorter than original
    assert len(result.split()) <= 20
    
    # Check that it ends with the end of the original text
    assert sample_text.strip().endswith(result.strip())


def test_truncate_middle_tokens(sample_text):
    """Test truncation from the middle with token limit."""
    truncator = PrecisionTruncator(max_tokens=30)
    result = truncator.truncate(sample_text, TruncationStrategy.MIDDLE)
    
    # Check if result is shorter than original
    assert len(result.split()) <= 32  # Allow for [...] marker
    
    # Check that it contains the marker
    assert "[...]" in result


def test_truncate_smart_tokens(sample_text):
    """Test smart truncation with token limit."""
    truncator = PrecisionTruncator(max_tokens=30)
    result = truncator.truncate(sample_text, TruncationStrategy.SMART)
    
    # Check if result is shorter than original
    assert len(result.split()) <= 30
    
    # Smart truncation should include important terms
    assert "artificial intelligence" in result.lower()


def test_truncate_chars(sample_text):
    """Test character-based truncation."""
    truncator = PrecisionTruncator(max_chars=100)
    result = truncator.truncate(sample_text, TruncationStrategy.START)
    
    # Check if result is shorter than original
    assert len(result) <= 100


def test_keep_sentences(sample_text):
    """Test sentence preservation option."""
    truncator = PrecisionTruncator(max_tokens=20)
    
    # With sentence preservation
    result_with = truncator.truncate(sample_text, TruncationStrategy.START, keep_sentences=True)
    
    # Without sentence preservation
    result_without = truncator.truncate(sample_text, TruncationStrategy.START, keep_sentences=False)
    
    # Result with sentence preservation should end with punctuation
    assert result_with.strip()[-1] in ".!?"
    
    # Unless by chance, the results should be different
    assert result_with != result_without


def test_accept_string_strategy(sample_text):
    """Test that string strategy names are accepted."""
    truncator = PrecisionTruncator(max_tokens=20)
    
    # Using string instead of enum
    result = truncator.truncate(sample_text, "start")
    
    # Should not raise an error
    assert isinstance(result, str)


def test_invalid_strategy(sample_text):
    """Test that invalid strategies raise errors."""
    truncator = PrecisionTruncator(max_tokens=20)
    
    with pytest.raises(ValueError):
        truncator.truncate(sample_text, "invalid_strategy")


def test_no_truncation_needed(sample_text):
    """Test that no truncation occurs if text is already short enough."""
    # Create a truncator with a very large limit
    truncator = PrecisionTruncator(max_tokens=1000)
    result = truncator.truncate(sample_text, TruncationStrategy.START)
    
    # Result should be identical to input
    assert result.strip() == sample_text.strip()