"""
Core truncation functionality for the Precision Truncator.
"""

from enum import Enum
import re
from typing import List, Union, Optional
from .utils import count_tokens, extract_key_sentences


class TruncationStrategy(Enum):
    """Available truncation strategies."""
    START = "start"  # Keep the start of the text
    END = "end"  # Keep the end of the text
    MIDDLE = "middle"  # Keep both start and end, truncate the middle
    SMART = "smart"  # Use semantic analysis to keep important parts


class PrecisionTruncator:
    """
    A tool for smart text truncation that preserves context.
    
    This class provides various methods to truncate text while maintaining
    the most relevant information based on different strategies.
    """
    
    def __init__(self, max_tokens: Optional[int] = None, max_chars: Optional[int] = None):
        """
        Initialize the truncator with maximum limits.
        
        Args:
            max_tokens: Maximum number of tokens to keep (if using token-based truncation)
            max_chars: Maximum number of characters to keep (if using character-based truncation)
        """
        if max_tokens is None and max_chars is None:
            raise ValueError("Either max_tokens or max_chars must be specified")
        
        self.max_tokens = max_tokens
        self.max_chars = max_chars
    
    def truncate(self, 
                 text: str, 
                 strategy: Union[TruncationStrategy, str] = TruncationStrategy.SMART,
                 keep_sentences: bool = True) -> str:
        """
        Truncate text according to the specified strategy.
        
        Args:
            text: The text to truncate
            strategy: The truncation strategy to use
            keep_sentences: Whether to preserve complete sentences
            
        Returns:
            The truncated text
        """
        if isinstance(strategy, str):
            strategy = TruncationStrategy(strategy)
            
        # Check if truncation is needed
        if self.max_tokens and count_tokens(text) <= self.max_tokens:
            return text
        if self.max_chars and len(text) <= self.max_chars:
            return text
            
        # Apply the selected strategy
        if strategy == TruncationStrategy.START:
            return self._truncate_start(text, keep_sentences)
        elif strategy == TruncationStrategy.END:
            return self._truncate_end(text, keep_sentences)
        elif strategy == TruncationStrategy.MIDDLE:
            return self._truncate_middle(text, keep_sentences)
        elif strategy == TruncationStrategy.SMART:
            return self._truncate_smart(text, keep_sentences)
        else:
            raise ValueError(f"Unknown truncation strategy: {strategy}")
    
    def _truncate_start(self, text: str, keep_sentences: bool) -> str:
        """Keep the start of the text."""
        if self.max_tokens:
            # Token-based truncation
            tokens = text.split()  # Simple word-based tokenization
            if keep_sentences:
                return self._reconstruct_sentences(tokens[:self.max_tokens])
            return " ".join(tokens[:self.max_tokens])
        else:
            # Character-based truncation
            if keep_sentences:
                return self._truncate_to_sentence_boundary(text[:self.max_chars])
            return text[:self.max_chars]
    
    def _truncate_end(self, text: str, keep_sentences: bool) -> str:
        """Keep the end of the text."""
        if self.max_tokens:
            # Token-based truncation
            tokens = text.split()
            if keep_sentences:
                return self._reconstruct_sentences(tokens[-self.max_tokens:])
            return " ".join(tokens[-self.max_tokens:])
        else:
            # Character-based truncation
            if keep_sentences:
                return self._truncate_to_sentence_boundary(text[-self.max_chars:], from_start=False)
            return text[-self.max_chars:]
    
    def _truncate_middle(self, text: str, keep_sentences: bool) -> str:
        """Keep both the start and end of the text, truncate the middle."""
        if self.max_tokens:
            tokens = text.split()
            if len(tokens) <= self.max_tokens:
                return text
                
            # Keep half from start, half from end
            half_tokens = self.max_tokens // 2
            start_tokens = tokens[:half_tokens]
            end_tokens = tokens[-half_tokens:]
            
            if keep_sentences:
                start_text = self._reconstruct_sentences(start_tokens)
                end_text = self._reconstruct_sentences(end_tokens)
            else:
                start_text = " ".join(start_tokens)
                end_text = " ".join(end_tokens)
                
            return f"{start_text} [...] {end_text}"
        else:
            # Character-based truncation
            if len(text) <= self.max_chars:
                return text
                
            half_chars = self.max_chars // 2
            start_text = text[:half_chars]
            end_text = text[-half_chars:]
            
            if keep_sentences:
                start_text = self._truncate_to_sentence_boundary(start_text)
                end_text = self._truncate_to_sentence_boundary(end_text, from_start=False)
                
            return f"{start_text} [...] {end_text}"
    
    def _truncate_smart(self, text: str, keep_sentences: bool) -> str:
        """Use semantic analysis to keep important parts."""
        # Extract key sentences that fit within our limits
        sentences = extract_key_sentences(text)
        
        result = ""
        current_length = 0
        
        for sentence in sentences:
            # Check if adding this sentence would exceed our limit
            sentence_length = count_tokens(sentence) if self.max_tokens else len(sentence)
            
            if current_length + sentence_length <= (self.max_tokens or self.max_chars):
                result += sentence + " "
                current_length += sentence_length
            else:
                break
                
        return result.strip()
    
    def _truncate_to_sentence_boundary(self, text: str, from_start: bool = True) -> str:
        """Adjust truncation to respect sentence boundaries."""
        # Simple regex for sentence boundaries (period, question mark, exclamation)
        sentence_end = r'[.!?]'
        
        if from_start:
            # Find the last sentence boundary
            matches = list(re.finditer(sentence_end, text))
            if matches:
                last_match = matches[-1]
                return text[:last_match.end()]
        else:
            # Find the first sentence boundary
            match = re.search(sentence_end, text)
            if match:
                return text[match.end():]
                
        return text  # Return original if no sentence boundary found
    
    def _reconstruct_sentences(self, tokens: List[str]) -> str:
        """Reconstruct complete sentences from tokens."""
        text = " ".join(tokens)
        return self._truncate_to_sentence_boundary(text)