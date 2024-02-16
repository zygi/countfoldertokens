import tiktoken
import argparse
import pathlib
import os
import concurrent.futures
import tqdm
import sys
import contextlib

# set up cli arguments
parser = argparse.ArgumentParser(description='Count tokens in a folder')
parser.add_argument('folder', type=str, help='folder to count tokens in')
parser.add_argument('--pattern', type=str, required=False, help='pattern to match files against')
parser.add_argument('--tokenizer', type=str, default="cl100k_base", help='tokenizer to use')
parser.add_argument('-q', '--quiet', type=bool, default=False, help='tokenizer to use')

def initializer(tok_name):
    global enc
    enc = tiktoken.get_encoding(tok_name)
    
def token_count(file):
    global enc
    with open(file, "r") as f:
        text = f.read()
    return len(enc.encode(text))

def main():
    args = parser.parse_args()
    folder = args.folder
    assert isinstance(folder, str)
    
    # get file tree recursively
    files = list(pathlib.Path(folder).glob("**/*" if args.pattern is None else args.pattern))
    
    
    with concurrent.futures.ProcessPoolExecutor(initializer=initializer, initargs=(args.tokenizer,)) as executor:
        context = contextlib.nullcontext() if args.quiet else tqdm.tqdm(total=len(files))
        with context as pbar:
            futures = {executor.submit(token_count, file): file for file in files}
            tok_counts = []
            for future in concurrent.futures.as_completed(futures):
                tok_counts.append(future.result())
                if not args.quiet:
                    pbar.update(1)
    
    print(sum(tok_counts))

    