import argparse
import logging
import dataclasses
import re
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from markdown_pdf import MarkdownPdf, Section


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def read_data(input_path: str) -> str:
    """Read PDF data from a specified input path.
    
    Args:
        input_path (str): Path to the input PDF file.
        
    Returns:
        str: Extracted text from the PDF.
    """
    converter = PdfConverter(
        artifact_dict=create_model_dict(),
    )
    rendered = converter(input_path)
    text, *_ = text_from_rendered(rendered)
    return text


def read_markdown(input_path: str) -> str:
    """Read the content of a markdown file.
    
    Args:
        input_path (str): The file path of a markdown file.
        
    Returns:
        str: The content of the markdown file.
    """
    with open(input_path, mode="r", encoding="utf-8") as f:
        return f.read()


@dataclasses.dataclass
class Card:
    """Data structure for a card."""
    title: str
    content: str


def split_text_into_cards(text: str, title_pattern: str, header_pattern: str) -> list[Card]:
    """Split the text into cards based on some criteria.
    
    Args:
        text (str): The text to be split into cards.
        title_pattern (str): Regular expression pattern to identify card titles.
        header_pattern (str): Regular expression pattern to identify card headers.
        
    Returns:
        list[Card]: A list of Card objects.
    """
    lines = text.splitlines()

    cards = []
    current_title = ""
    current_content = ""

    for line in lines:
        title_match = re.search(title_pattern, line)
        # If we find a new title, we save the current card and start a new one
        if title_match:
            if current_title:
                cards.append(Card(title=current_title, content=current_content))
            # Start a new card
            current_title = line.strip()
            current_content = ""
        else:
            # If the line matches the header pattern, we append it to the current title
            header_match = re.search(header_pattern, line)
            if header_match and current_title:
                current_title += f"{line.strip()}\n"
        
        current_content += f"{line.strip()}\n"

    if current_title:
        cards.append(Card(title=current_title, content=current_content))
    
    return cards


def write_cards(output_path: str, cards: list[Card]) -> None:
    """Write data to a specified output path."""
    pdf = MarkdownPdf(optimize=True)
    for card in cards:
        pdf.add_section(Section(card.title, toc=False, paper_size="A5"))
        pdf.add_section(Section(card.content, toc=False, paper_size="A3"))
    pdf.save(output_path)  


def main():
    parser = argparse.ArgumentParser(description="PDF Cards Generator")
    parser.add_argument(
        "--input",
        type=str,
        help="Path to the input PDF file information used to create the cards.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to the output directory where the generated cards will be saved.",
    )
    parser.add_argument(
        "--title_pattern",
        type=str,
        default="^#+\*\*(\d+\.\d+)",
        help="Regular expression pattern to identify card titles.",
    )
    parser.add_argument(
        "--header_pattern",
        type=str,
        default="^#+",
        help="Regular expression pattern to identify card heades that are added to the card titles.",
    )
    parser.add_argument(
        "--markdown",
        type=str,
        default=None,
        help="An optional markdown input file. If this is provided we skip the PDF file to to markdown conversion and only read the markdown file."
    )

    args = parser.parse_args()
    logger.info("Starting PDF Cards Generator")
    logger.info(f"Input file: {args.input}")
    logger.info(f"Output directory: {args.output}")
    logger.info(f"Title pattern: {args.title_pattern}")
    logger.info(f"Header pattern: {args.header_pattern}")
    logger.info(f"Markdown file: {args.markdown}")

    if args.markdown:
        data = read_markdown(args.markdown)
        logger.info("Data read successfully from the markdown file.")
    else:
        assert args.input, "You either have to provide a PDF input file via `--input` or a markdown file with `--markdown`!"
        data = read_data(args.input)
        logger.info("Data read successfully from the input file.")

    cards = split_text_into_cards(data, title_pattern=args.title_pattern, header_pattern=args.header_pattern)
    logger.info(f"Generated {len(cards)} cards from the input data.")
    write_cards(args.output, cards)
    logger.info("Data written successfully to the output directory.")

if __name__ == "__main__":
    main()