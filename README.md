# OPML Exporter

A command-line interface (CLI) to export Apple Podcasts to OPML files. Based on [Exporting OPML feed from Apple Podcasts](https://bitsden.com/posts/2022/02/exporting-opml-from-apple-podcasts/) by [Marcus Ramsden](https://bitsden.com/)

## 🎧 Quick Start

Ensure [Python](https://www.python.org/downloads) and [Python Poetry](https://python-poetry.org/docs/#installation) are installed.

Dependency installation is managed via `poetry`. Once cloned, you can install dependencies from the project root:

```shell
poetry install
```

Once dependencies are installed, you can run the exporter:

```shell
poetry run opml-exporter
```

And huzzah! You're ready to export some podcasts! 🎉

## 🧪 Running Tests

[`pytest`](https://docs.pytest.org/en/7.2.x/) is used as a test runner and its configuration can be found in the `tool.pytest.ini_options` section of [pyproject.toml](./pyproject.toml). [`pytest-cov`](https://pytest-cov.readthedocs.io/en/latest/index.html) is used as a coverage reporter.

Running `pytest` with no arguments will:

- Automatically add `src` to `PYTHONPATH` (pythonpath: `src`)
- Only run unit tests (testpaths: `tests/opml_exporter`)
- Increase verbosity (`-vv`)
- Calculate coverage (using `pytest-cov`) and display any modules missing coverage

## 🪪 License

This tool is [MIT licensed](./LICENSE).
