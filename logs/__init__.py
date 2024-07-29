import os
import logging
from config.config import Config

def setup_logger():
    if not os.path.exists(Config.LOG_DIR):
        os.makedirs(Config.LOG_DIR)
    logging.basicConfig(filename=os.path.join(Config.LOG_DIR, "ap_news.log"),
                        level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(__name__)