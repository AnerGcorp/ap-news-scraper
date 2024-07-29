import sys
import logging
from logs import setup_logger
from src.news_scraper import NewsScraper
from robocorp.tasks import task

@task
def scraper(search_phrase, months):
    setup_logger()
    logger = logging.getLogger(__name__)

    logger.info(f"Starting the news scraper...")
    scraper = NewsScraper(search_phrase, months)
    logger.info("Started processing...")
    scraper.run()
    logger.info(f"News scraper finished successfully.")

if __name__ == "__main__":
    # Example parameters, these would be provided by Robocloudworkitem in real case scenario
    if len(sys.argv) < 3:
        print("Usage: python main.py <search_phrase> <months>")
        sys.exit(1)

    search_phrase = sys.argv[1]
    months = int(sys.argv[2])
    scraper(search_phrase, months)