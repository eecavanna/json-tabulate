# json-tabulate

Python library and CLI program that translates arbitrarily-nested JSON into CSV

## Development

Install dependencies:

```sh
uv sync
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
```
