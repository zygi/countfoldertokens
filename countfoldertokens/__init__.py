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
parser.add_argument('--pattern', type=str, required=False, help='Pattern to match files against.')
parser.add_argument('--tokenizer', type=str, default="cl100k_base", help='Tokenizer to use. Any tokenizer from the `tiktoken` package can be used.')
parser.add_argument('--progress', action=argparse.BooleanOptionalAction, default=True, help='Show a progress bar. Default: True')
parser.add_argument('--respect-gitignore', action=argparse.BooleanOptionalAction, default=True, help='Respect .gitignore files. Default: True')
parser.add_argument('--verbose', action=argparse.BooleanOptionalAction, help='Print information about processed files. Default: False')

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

def filter_gitignore(start_folder, files):
    import git
    try:
        repo = git.Repo(start_folder, search_parent_directories=True)
        ignored = set(repo.ignored(files))
        # print(ignored)
        # print([str(f) for f in files])
        notignored = {f for f in files if str(f) not in ignored}
        repo.close()
        return notignored
    except git.InvalidGitRepositoryError:
        return files

def main():
    args = parser.parse_args()
    folder = args.folder
    assert isinstance(folder, str)
    
    # get file tree recursively
    files = list(e for e in pathlib.Path(folder).glob("**/*" if args.pattern is None else args.pattern) if e.is_file())
    
    if args.respect_gitignore:
        files = filter_gitignore(folder, files)
        # also filter out .git directories
        files = [f for f in files if not ".git" in f.parts and f.name != ".gitignore"]
    
    with concurrent.futures.ProcessPoolExecutor(initializer=initializer, initargs=(args.tokenizer,)) as executor:
        context = tqdm.tqdm(total=len(files)) if args.progress else contextlib.nullcontext()
        with context as pbar:
            futures = {executor.submit(token_count, file): file for file in files}
            tok_counts = []
            for future in concurrent.futures.as_completed(futures):
                filename, tok_count = future.result()
                if tok_count is not None:
                    tok_counts.append(tok_count)
                if args.progress:
                    pbar.update(1)
                if args.verbose:
                    print(f"{filename}: {tok_count}")
    
    print(sum(tok_counts))

    