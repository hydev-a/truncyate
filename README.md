# Truncayte - Precision Truncator

A smart text truncation tool for RAG systems and LLMs that preserves context while reducing text to desired lengths.

![PyPI Version](https://img.shields.io/badge/pypi-0.1.0-blue.svg)
![Python Versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- Multiple truncation strategies:
  - **Start**: Keep the beginning of the text
  - **End**: Keep the ending of the text
  - **Middle**: Keep both start and end, truncate the middle
  - **Smart**: Use semantic analysis to preserve the most important content
- Options for token-based or character-based truncation
- Sentence boundary preservation for more readable results
- Smart extraction of key sentences based on content signals
- Lightweight with minimal dependencies

## Installation

```bash
pip install precision-truncator
```

## Quick Start

```python
from precision_truncator import PrecisionTruncator, TruncationStrategy

# Create a truncator that limits text to 100 tokens
truncator = PrecisionTruncator(max_tokens=100)

# Sample text
long_text = """
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

AI applications include advanced web search engines, recommendation systems, 
understanding human speech, self-driving cars, automated decision-making, 
and competing at the highest level in strategic game systems. As machines 
become increasingly capable, tasks considered to require "intelligence" 
are often removed from the definition of AI, a phenomenon known as the 
AI effect.
"""

# Truncate using different strategies
start_truncated = truncator.truncate(long_text, TruncationStrategy.START)
end_truncated = truncator.truncate(long_text, TruncationStrategy.END)
middle_truncated = truncator.truncate(long_text, TruncationStrategy.MIDDLE)
smart_truncated = truncator.truncate(long_text, TruncationStrategy.SMART)

print(f"Start strategy:\n{start_truncated}\n")
print(f"End strategy:\n{end_truncated}\n")
print(f"Middle strategy:\n{middle_truncated}\n")
print(f"Smart strategy:\n{smart_truncated}\n")
```

## Advanced Usage

### Character-Based Truncation

```python
# Character-based truncation (limit to 200 characters)
char_truncator = PrecisionTruncator(max_chars=200)
result = char_truncator.truncate(long_text, TruncationStrategy.SMART)
```

### Control Sentence Preservation

```python
# Disable sentence preservation for more precise truncation length
truncator = PrecisionTruncator(max_tokens=100)
result = truncator.truncate(long_text, TruncationStrategy.SMART, keep_sentences=False)
```

## Use Cases

- **RAG Systems**: Truncate retrieved documents while preserving the most relevant content
- **Context Windows**: Optimize usage of limited context windows in LLMs
- **API Limitations**: Stay within character or token limits for API requests
- **User Interfaces**: Generate meaningful previews or snippets of longer texts
- **Data Processing**: Efficiently handle large text documents in NLP pipelines

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.