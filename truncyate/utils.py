"""
Utility functions for the Precision Truncator.
"""

import re
from typing import List, Dict, Tuple
import spacy
import sys

# Load spaCy model (do this once at module level to avoid reloading)
nlp = spacy.load("en_core_web_lg")  # Use 'en_core_web_sm' for smaller footprint

def count_tokens(text: str) -> int:
    """
    Count the approximate number of tokens in the text using spaCy's tokenizer.
    
    Args:
        text: The text to count tokens for
        
    Returns:
        The token count
    """
    doc = nlp(text)
    return len(doc)

def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences using spaCy.
    
    Args:
        text: The text to split
        
    Returns:
        A list of sentences
    """
    text = handle_abbreviations(text)  # Preprocess abbreviations
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    return sentences

def calculate_sentence_importance(sentence: str, position: int, total_sentences: int, doc: spacy.tokens.Doc) -> float:
    """
    Calculate importance score using spaCy features.
    
    Args:
        sentence: The sentence to score
        position: Sentence position in the text
        total_sentences: Total number of sentences
        doc: spaCy Doc object for the entire text (to avoid reprocessing)
        
    Returns:
        Importance score
    """
    score = 0.0
    
    # Process sentence with spaCy
    sent_doc = nlp(sentence)
    
    # Position-based scoring
    if position == 0 or position == total_sentences - 1:
        score += 0.3
    elif position <= 2 or position >= total_sentences - 3:
        score += 0.2
    
    # Length-based scoring
    if len(sent_doc) > 10:
        score += 0.1
    
    # Entity-based scoring
    entities = [ent.text for ent in sent_doc.ents if ent.label_ in ("PERSON", "ORG", "GPE", "DATE", "EVENT")]
    if entities:
        score += 0.15 * len(entities)  # Boost for each entity
    
    # Keyword-based scoring
    importance_indicators = {
        "important", "significant", "crucial", "essential", "critical",
        "conclusion", "therefore", "thus", "result", "summary",
        "first", "second", "third", "finally", "lastly",
        "must", "should", "key", "main"
    }
    for token in sent_doc:
        if token.lemma_.lower() in importance_indicators:
            score += 0.2
            break
    
    # Semantic similarity to the entire document
    if doc.has_vector and sent_doc.has_vector:
        similarity = sent_doc.similarity(doc)
        score += similarity * 0.3  # Weight similarity (0 to 1) by 0.3
    print(f"DEBUG: Sentence: '{sentence}', Score: {score}, Entities: {entities}, Similarity: {similarity if doc.has_vector else 'N/A'}", file=sys.stderr)
    return score

def extract_key_sentences(text: str) -> List[str]:
    """
    Extract key sentences using spaCy for semantic analysis.
    
    Args:
        text: The text to analyze
        
    Returns:
        A list of sentences ordered by importance
    """
    sentences = split_into_sentences(text)
    if not sentences:
        return []
    
    # Process the entire text once with spaCy
    doc = nlp(text)
    
    # Score sentences
    scored_sentences = []
    for i, sentence in enumerate(sentences):
        score = calculate_sentence_importance(sentence, i, len(sentences), doc)
        scored_sentences.append((sentence, score))
    
    # Sort by score (highest first)
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in scored_sentences]

def handle_abbreviations(text: str) -> str:
    """
    Process text to handle common abbreviations that might confuse sentence splitting.
    
    Args:
        text: The text to process
        
    Returns:
        Text with abbreviations handled
    """
    common_abbrev = [
        "Mr.", "Mrs.", "Ms.", "Dr.", "Prof.",
        "Inc.", "Ltd.", "Co.", "Corp.",
        "i.e.", "e.g.", "etc.", "vs.", "a.m.", "p.m."
    ]
    for abbr in common_abbrev:
        text = text.replace(abbr, abbr.replace(".", "<<DOT>>"))
    return text

def extract_entities(text: str) -> Dict[str, int]:
    """
    Extract named entities from text with simple heuristics.
    
    Args:
        text: The text to analyze
        
    Returns:
        A dictionary of entity names and their frequency
    """
    capitalized_phrases = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', text)
    entities = {}
    for phrase in capitalized_phrases:
        if len(phrase.split()) >= 1:
            entities[phrase] = entities.get(phrase, 0) + 1
    return entities