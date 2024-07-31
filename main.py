import os
import logging
from logs import setup_logger
from src.news_scraper import NewsScraper
from robocorp.tasks import task
from robocorp import workitems

@task
def scraper():
    setup_logger()
    logger = logging.getLogger(__name__)

    input_data = workitems.inputs.current.payload
    logger.info(f"Input data: {input_data}")  # This will print the input data as a dictionary

    search_phrase = input_data.get('SEARCH_PHRASE', "imagination")
    months = int(input_data.get('MONTHS', '1'))  # Default to 1 month if MONTHS environment variable not set

    logger.info(f"Starting the news scraper...")
    scraper = NewsScraper(search_phrase, months)
    logger.info("Started processing...")
    scraper.run()
    logger.info(f"News scraper finished successfully.")

if __name__ == "__main__":
    # Example parameters, these would be provided by Robocloudworkitem in real case scenario
    
    scraper()