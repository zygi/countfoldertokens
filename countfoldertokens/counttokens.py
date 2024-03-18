# a miniscript to count tokens of an individual file, either from its path or from stdin

import tiktoken
import argparse
import sys
from typing import Optional

# set up cli arguments
parser = argparse.ArgumentParser(description='Count tokens of a file')
parser.add_argument('file', type=str, help='If provided, file to count tokens of. If empty, data will be read from stdin', nargs='?')
parser.add_argument('--tokenizer', type=str, default="cl100k_base", help='Tokenizer to use. Any tokenizer from the `tiktoken` package can be used.')

def initializer(tok_name):
    global enc
    enc = tiktoken.get_encoding(tok_name)
    
def token_count(file):
    global enc
    try:
        with open(file, "r") as f:
            text = f.read()
        return (file, len(enc.encode(text)))
    except UnicodeDecodeError:
        return (file, None)

def main():
    args = parser.parse_args()
    if args.file is not None:
        with open(args.file, "r") as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    
    enc = tiktoken.get_encoding(args.tokenizer)
    print(len(enc.encode(text)))

if __name__ == "__main__":
    main()