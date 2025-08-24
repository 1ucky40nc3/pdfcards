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
pdfcards --input data/example.pdf --output output/example-indexcards.pdf --title_pattern "^#+ \*\*(\d+\.\d+)" --header_pattern "^#+" --title_page_format "A5-L" --content_page_format "A3-L"
# Use marker to convert a PDF file into markdown and use the markdown as input for pdfcards
marker_single /path/to/file.pdf --output_format markdown --output_dir output/
pdfcards --markdown outputs/file.md --output output/card.pdf --title_pattern "^#+ \*\*(\d+\.\d+)" --header_pattern "^#+" --title_page_format "A5-L" --content_page_format "A3-L"
```

Using the `--page_range` argument you can optionally process selected PDF page ranges.

```bash
# Note: files in the ./data and ./output directories are hidden by the .gitignore file
# Note: In the following examples we select the PDF page 0, 5 to 10 and page 20
pdfcards --input data/example.pdf --output output/example-indexcards.pdf --title_pattern "^#+ \*\*(\d+\.\d+)" --header_pattern "^#+" --title_page_format "A5-L" --content_page_format "A3-L" --page_range "0,5-10,20"
# Use marker to convert a PDF file into markdown and use the markdown as input for pdfcards
marker_single /path/to/file.pdf --output_format markdown --output_dir output/ --page_range "0,5-10,20"
pdfcards --markdown outputs/file.md --output output/card.pdf --title_pattern "^#+ \*\*(\d+\.\d+)" --header_pattern "^#+" --title_page_format "A5-L" --content_page_format "A3-L"
```

## Documentation

The `pdfcards` script works by converting PDF files into markdown internally. Afterwards the markdown is split by headers. Based on the headers the index cards are created.

The PDF to markdown conversion is done using the [marker](https://github.com/datalab-to/marker?tab=readme-ov-file#marker) package.

Each index card consists of a **title** and (hidden) **content**. Titles primarily found using the `--title_pattern` regex. Additional information can be added to the titles (such as headers) using the `--header_pattern`. Each of the regex patterns match lines in the converted markdown text and add them to a cards title.
Every time a new line matches with `--title_pattern` regex we create a new card. Any line that does not match with a `--title_pattern` or `--header_pattern` regex is added to the content of a the current card.

At the end a output PDF is created. Every odd paged of the pdf is the title of a card. Every even page is the hidden content. Every odd page has the A5 size. Even pages have a A3 size to consolidate more information.