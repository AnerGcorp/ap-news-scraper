import os

class Config:
    OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
    LOG_DIR = os.path.join(os.getcwd(), 'output')
    NEWS_URL = "https://apnews.com/"