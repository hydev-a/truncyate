#!/usr/bin/env python
"""
Command-line interface for Precision Truncator.
"""

import argparse
import sys
from truncyate import PrecisionTruncator, TruncationStrategy


def main():
    """Run the Precision Truncator CLI."""
    parser = argparse.ArgumentParser(
        description="Precisely truncate text while preserving context."
    )
    
    # Required arguments
    parser.add_argument(
        "input",
        nargs="?",
        help="Input text to truncate. If not provided, reads from stdin.",
    )
    
    # Limit options (must specify one)
    limit_group = parser.add_mutually_exclusive_group(required=True)
    limit_group.add_argument(
        "--tokens", "-t",
        type=int,
        help="Maximum number of tokens to keep"
    )
    limit_group.add_argument(
        "--chars", "-c",
        type=int,
        help="Maximum number of characters to keep"
    )
    
    # Strategy selection
    parser.add_argument(
        "--strategy", "-s",
        choices=["start", "end", "middle", "smart"],
        default="smart",
        help="Truncation strategy to use (default: smart)"
    )
    
    # Additional options
    parser.add_argument(
        "--no-keep-sentences",
        action="store_false",
        dest="keep_sentences",
        help="Disable sentence preservation (truncate exactly to limit)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file (default: stdout)"
    )
    
    # Input file option
    parser.add_argument(
        "--input-file", "-f",
        help="Read input from file instead of argument or stdin"
    )
    
    args = parser.parse_args()
    
    # Get input text
    if args.input_file:
        try:
            with open(args.input_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading input file: {e}", file=sys.stderr)
            return 1
    elif args.input:
        text = args.input
    else:
        # Read from stdin
        text = sys.stdin.read()
    
    # Create truncator
    truncator = PrecisionTruncator(
        max_tokens=args.tokens,
        max_chars=args.chars
    )
    
    # Truncate text
    result = truncator.truncate(
        text,
        strategy=args.strategy,
        keep_sentences=args.keep_sentences
    )
    
    # Output result
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
        except Exception as e:
            print(f"Error writing to output file: {e}", file=sys.stderr)
            return 1
    else:
        print(result)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())