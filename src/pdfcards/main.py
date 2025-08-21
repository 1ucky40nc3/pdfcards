import argparse
import logging
import dataclasses
import re
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered


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
        if title_match:
            if current_title:
                cards.append(Card(title=current_title, content=current_content))
            current_title = line.strip()
        else:
            header_match = re.search(header_pattern, line)
            if header_match and current_title:
                current_title += f"{line.strip()}\n"
            else:
                current_content += f"{line.strip()}\n"
        print(current_title)
    if current_title:
        cards.append(Card(title=current_title, content=current_content))
    return cards

def write_cards(output_path: str, cards: list[Card]) -> None:
    """Write data to a specified output path."""


def main():
    parser = argparse.ArgumentParser(description="PDF Cards Generator")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
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

    args = parser.parse_args()
    logger.info("Starting PDF Cards Generator")
    logger.info(f"Input file: {args.input}")
    logger.info(f"Output directory: {args.output}")
    data = read_data(args.input)
    #print(data)
    logger.info("Data read successfully from the input file.")
    cards = split_text_into_cards(data, title_pattern=args.title_pattern, header_pattern=args.header_pattern)
    logger.info(f"Generated {len(cards)} cards from the input data.")
    print(cards)
    write_cards(args.output, cards)
    logger.info("Data written successfully to the output directory.")

if __name__ == "__main__":
    main()