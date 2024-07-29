import os

class Config:
    OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
    LOG_DIR = os.path.join(os.getcwd(), 'logs')
    NEWS_URL = "https://apnews.com/"