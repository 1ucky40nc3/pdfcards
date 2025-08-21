# pdfcards

Python Script to Convert PDF into Index Cards

## Getting Started

### Installation

You need to install the following requirements:

- (Optional: [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation))
- Python >= 3.12
- [poetry](https://python-poetry.org/docs/#installation)

Install the poetry dependencies and setup the project:

```bash
poetry install
```

## Examples

Exatract data from a PDF file and create index cards.

```bash
# Note: files in the ./data and ./output directories are hidden by the .gitignore file
pdfcards --input data/example.pdf --output outputs/example-indexcards.pdf --title_pattern "^#+\*\*(\d+\.\d+)" --header_pattern "^#+"
```

## Documentation

The `pdfcards` script works by converting PDF files into markdown internally. Afterwards the markdown is split by headers. Based on the headers the index cards are created.

The PDF to markdown conversion is done using the [marker](https://github.com/datalab-to/marker?tab=readme-ov-file#marker) package.

Each index card consists of a **title** and (hidden) **content**. Titles primarily found using the `--title_pattern` regex. Additional information can be added to the titles (such as headers) using the `--header_pattern`. Each of the regex patterns match lines in the converted markdown text and add them to a cards title.
Every time a new line matches with `--title_pattern` regex we create a new card. Any line that does not match with a `--title_pattern` or `--header_pattern` regex is added to the content of a the current card.

At the end a output PDF is created. Every odd paged of the pdf is the title of a card. Every even page is the hidden content.