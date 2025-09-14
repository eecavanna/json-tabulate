# json-tabulate

Python library and CLI program that translates arbitrarily-nested JSON into CSV

## Development

Install dependencies:

```sh
uv sync
```

Lint Python source code:

```sh
uv run ruff check
```

Format Python source code:

```sh
uv run ruff format

# Other option: Do a dry run.
uv run ruff format --diff
```

Run CLI program:

```sh
uv run json-tabulate --help
```

Import Python library:

```sh
uv run ptpython
>>> from json_tabulate import process_json
>>> process_json(json_input=r'{}')
''
>>> quit()
```
