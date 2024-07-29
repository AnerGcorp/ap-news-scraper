import logging
from logs import setup_logger
from src.news_scraper import NewsScraper

def main(search_phrase, months):
    setup_logger()
    logger = logging.getLogger(__name__)

    logger.info(f"Starting the news scraper...")
    scraper = NewsScraper(search_phrase, months)
    logger.info("Started processing...")
    scraper.run()
    logger.info(f"News scraper finished successfully.")

if __name__ == "__main__":
    # Example parameters, these would be provided by Robocloudworkitem in real case scenario
    search_phrase = "technology"
    months = 1
    main(search_phrase, months)