A small utility script to count how many tokens of text a given folder contains.

## Install
Either clone and install manually, or using [pipx](https://pipx.pypa.io/stable/)
```
pipx run --spec=git+https://github.com/zygi/countfoldertokens.git countfoldertokens <ARGS>
```

## Examples

```
countfoldertokens .
```

```
countfoldertokens . --pattern "**/*.py" --verbose
```

```
countfoldertokens . --no-progress-bar | (read x; echo "Saw $x tokens")
```

## Arguments

```
usage: -c [-h] [--pattern PATTERN] [--tokenizer TOKENIZER] [--progress | --no-progress] [--respect-gitignore | --no-respect-gitignore] [--verbose | --no-verbose] folder

Count tokens in a folder

positional arguments:
  folder                folder to count tokens in

options:
  -h, --help            show this help message and exit
  --pattern PATTERN     Pattern to match files against.
  --tokenizer TOKENIZER
                        Tokenizer to use. Any tokenizer from the `tiktoken` package can be used.
  --progress, --no-progress
                        Show a progress bar. Default: True
  --respect-gitignore, --no-respect-gitignore
                        Respect .gitignore files. Default: True
  --verbose, --no-verbose
                        Print information about processed files. Default: False
```