"""
Utility functions for the Precision Truncator.
"""

import re
from typing import List, Dict, Tuple


def count_tokens(text: str) -> int:
    """
    Count the approximate number of tokens in the text.
    
    This is a simple implementation that counts words as tokens.
    For more accurate token counting with specific models like GPT,
    you would need to use model-specific tokenizers.
    
    Args:
        text: The text to count tokens for
        
    Returns:
        The approximate token count
    """
    # Simple word-based tokenization
    return len(text.split())


def extract_key_sentences(text: str) -> List[str]:
    """
    Extract key sentences from the text based on importance signals.
    
    This implementation uses simple heuristics to identify important sentences:
    - Sentences containing keywords/phrases like "important", "in conclusion", etc.
    - Sentences at the beginning and end of paragraphs
    - Sentences containing numerical data or dates
    
    Args:
        text: The text to analyze
        
    Returns:
        A list of sentences ordered by estimated importance
    """
    # Split text into sentences
    sentences = split_into_sentences(text)
    
    # If no sentences, return empty list
    if not sentences:
        return []
    
    # Calculate importance scores for each sentence
    scored_sentences = []
    for i, sentence in enumerate(sentences):
        score = calculate_sentence_importance(sentence, i, len(sentences))
        scored_sentences.append((sentence, score))
    
    # Sort sentences by importance score (highest first)
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    
    # Return sentences in original order (more natural reading)
    sentence_order = {s: i for i, s in enumerate(sentences)}
    return [s[0] for s in sorted(scored_sentences, key=lambda x: sentence_order[x[0]])]


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences.
    
    Args:
        text: The text to split
        
    Returns:
        A list of sentences
    """
    # Handle common abbreviations to avoid false sentence breaks
    text = handle_abbreviations(text)
    
    # Split on sentence boundaries
    # This is a simple implementation - it may not handle all edge cases
    sentence_boundaries = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
    sentences = re.split(sentence_boundaries, text)
    
    # Clean up sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def handle_abbreviations(text: str) -> str:
    """
    Process text to handle common abbreviations that might confuse sentence splitting.
    
    Args:
        text: The text to process
        
    Returns:
        Text with abbreviations handled
    """
    # Replace common abbreviations temporarily
    common_abbrev = [
        "Mr.", "Mrs.", "Ms.", "Dr.", "Prof.",
        "Inc.", "Ltd.", "Co.", "Corp.",
        "i.e.", "e.g.", "etc.", "vs.", "a.m.", "p.m."
    ]
    
    temp_text = text
    for abbr in common_abbrev:
        # Replace period with a special marker
        temp_text = temp_text.replace(abbr, abbr.replace(".", "<<DOT>>"))
    
    return temp_text


def calculate_sentence_importance(sentence: str, position: int, total_sentences: int) -> float:
    """
    Calculate the importance score for a sentence.
    
    Args:
        sentence: The sentence to score
        position: The position of the sentence in the text
        total_sentences: The total number of sentences in the text
        
    Returns:
        A score representing the estimated importance
    """
    score = 0.0
    
    # Position-based scoring (sentences at beginning and end often more important)
    if position == 0 or position == total_sentences - 1:
        score += 0.3
    elif position <= 2 or position >= total_sentences - 3:
        score += 0.2
        
    # Length-based scoring (very short sentences often less important)
    words = sentence.split()
    if len(words) > 10:
        score += 0.1
    
    # Keyword-based scoring
    importance_indicators = [
        "important", "significant", "crucial", "essential", "critical",
        "conclusion", "therefore", "thus", "result", "summary",
        "first", "second", "third", "finally", "lastly",
        "must", "should", "key", "main"
    ]
    
    for word in words:
        word_lower = word.lower().strip(".,;:!?")
        if word_lower in importance_indicators:
            score += 0.2
            break
    
    # Check for numerical data (often important)
    if re.search(r'\d+(?:\.\d+)?%?', sentence):
        score += 0.15
    
    # Check for dates
    if re.search(r'\b\d{4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b', sentence):
        score += 0.1
    
    # Check for quoted text (often important)
    if '"' in sentence or "'" in sentence:
        score += 0.1
    
    return score


def extract_entities(text: str) -> Dict[str, int]:
    """
    Extract named entities from text with simple heuristics.
    
    Args:
        text: The text to analyze
        
    Returns:
        A dictionary of entity names and their frequency
    """
    # Simple capitalized phrase detection (not a proper NER)
    # This is just a placeholder for a more sophisticated NER solution
    capitalized_phrases = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', text)
    
    entities = {}
    for phrase in capitalized_phrases:
        if len(phrase.split()) >= 1:  # Only consider phrases with at least one word
            entities[phrase] = entities.get(phrase, 0) + 1
    
    return entities