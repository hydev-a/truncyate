## README.md

#### ⚠️ Important note: This tiny project was developed entirely for proof of concept, demonstration and skill refining purposes, expect bugs and issues. I will include the project as a python package once I am satisfied with the development. 

# 🧠 Precision Truncator

A smart text truncation tool for RAG systems and LLMs that **preserves context** while reducing text to desired lengths.

---

## 🚀 Features

- **Multiple Truncation Strategies**:
  - `start`: Keep the beginning of the text
  - `end`: Keep the ending of the text
  - `middle`: Keep both start and end, truncate the middle
  - `smart`: Semantic analysis to retain the most important content

- Token-based or character-based truncation
- Sentence boundary preservation for cleaner, more readable output
- Smart extraction of key sentences using content signals
- Lightweight with minimal dependencies

---

## 📦 Installation

> ⚠️ Not available on PyPI yet.

1. **Clone the repository**:

   ```bash
   git clone https://github.com/hydev-a/truncyate.git
   cd truncyate
   ```

2. **Install in development mode**:

   ```bash
   pip install -e .
   ```
   
3. **Make sure spaCy's model is installed**: 

   ```bash
   python -m spacy download en_core_web_lg
   ```
> ⚠️ a lighter en_core_web_sm version is to be released with optimized performance.

This installs the package system-wide and lets you modify the code as needed.

---

## 🧪 Quick Start

```python
from truncyate import PrecisionTruncator, TruncationStrategy

# Create a truncator to limit to 100 tokens
truncator = PrecisionTruncator(max_tokens=100)

# Sample long text
long_text = """
Artificial intelligence (AI) is intelligence demonstrated by machines...
"""

# Apply truncation strategies
start_truncated = truncator.truncate(long_text, TruncationStrategy.START)
end_truncated = truncator.truncate(long_text, TruncationStrategy.END)
middle_truncated = truncator.truncate(long_text, TruncationStrategy.MIDDLE)
smart_truncated = truncator.truncate(long_text, TruncationStrategy.SMART)

print("Start strategy:\n", start_truncated)
print("End strategy:\n", end_truncated)
print("Middle strategy:\n", middle_truncated)
print("Smart strategy:\n", smart_truncated)
```

---

## 💻 Command-Line Usage

> ⚠️ This project was not meant to include a CLI initially. Some features may not work as expected (yet).

### Basic Examples

```bash
# Truncate to 50 tokens
truncyate "Your very long text goes here..." --tokens 50

# Truncate file and save output
truncyate --input-file document.txt --output truncated.txt --tokens 100

# Character-based truncation
truncyate "Your text..." --chars 200
```

### Truncation Strategies

```bash
# Keep the beginning
truncyate "Your text..." --tokens 50 --strategy start

# Keep the ending
truncyate "Your text..." --tokens 50 --strategy end

# Keep start + end, truncate middle
truncyate "Your text..." --tokens 50 --strategy middle

# Smart truncation (default)
truncyate "Your text..." --tokens 50 --strategy smart
```

### Piping and Sentence Options

```bash
# Pipe input from another command
cat document.txt | truncyate --tokens 100 > truncated.txt

# Disable sentence preservation
truncyate "Your text..." --tokens 50 --no-keep-sentences
```

---

## 🔁 Example Workflow

```bash
# Create sample text
echo "This is a sample text file with multiple sentences..." > sample.txt

# Smart truncation
truncyate --input-file sample.txt --tokens 20 --strategy smart

# Compare strategies
echo "START STRATEGY:" > comparison.txt
truncyate --input-file sample.txt --tokens 20 --strategy start >> comparison.txt

echo "\nEND STRATEGY:" >> comparison.txt
truncyate --input-file sample.txt --tokens 20 --strategy end >> comparison.txt

echo "\nMIDDLE STRATEGY:" >> comparison.txt
truncyate --input-file sample.txt --tokens 20 --strategy middle >> comparison.txt

echo "\nSMART STRATEGY:" >> comparison.txt
truncyate --input-file sample.txt --tokens 20 --strategy smart >> comparison.txt

cat comparison.txt
```

---

## 🛠️ Advanced Usage

### Character-Based Truncation

```python
char_truncator = PrecisionTruncator(max_chars=200)
result = char_truncator.truncate(long_text, TruncationStrategy.SMART)
```

### Disable Sentence Preservation

```python
truncator = PrecisionTruncator(max_tokens=100)
result = truncator.truncate(long_text, TruncationStrategy.SMART, keep_sentences=False)
```

---

## 🎯 Use Cases

* **RAG Systems**: Truncate documents without losing core meaning
* **LLM Context Windows**: Fit long data into limited model input
* **API Constraints**: Stay within token/char limits for requests
* **User Interfaces**: Generate previews/snippets of long content
* **Data Processing Pipelines**: Efficiently manage large documents

---

## 🤝 Contributing

Contributions are welcome! Follow these steps:

```bash
# Fork and clone
git clone https://github.com/yourusername/truncyate.git

# Create a new branch
git checkout -b feature-name

# Commit your changes
git commit -m 'Add some feature'

# Push to GitHub
git push origin feature-name

# Open a Pull Request
```

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.