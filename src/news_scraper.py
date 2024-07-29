from src.selenium_wrapper import SeleniumWrapper
from src.utils import (
    extract_money, 
    save_to_excel, 
    save_images_with_threadpoolexecutor, 
    extract_info, 
    extract_date,
    count_phrases,
    calculate_month_difference)
from config.config import Config
import logging

class NewsScraper:
    def __init__(self, search_phrase, months):
        self.search_phrase = search_phrase
        self.months = months
        self.selenium = SeleniumWrapper()
        self.logger = logging.getLogger(__name__)

    def run(self):
        try:
            self.selenium.open_page(Config.NEWS_URL)
            self.selenium.accept_cookies()
            self.selenium.search(self.search_phrase)
            self.selenium.sort("Newest")
           
            articles_list = []
            articles = self.selenium.get_news_articles(self.search_phrase)
            articles_list.extend(self.get_articles_list(articles))
            
            months = calculate_month_difference(extract_date(articles[-1].get_attribute('outerHTML')))
            while self.months >= months:
                try:
                    next = self.selenium.next_page()
                    if not next:
                        break
                    articles = self.selenium.get_news_articles(self.search_phrase)
                    if not articles:
                        break
                    articles_list.extend(self.get_articles_list(articles))
                    
                    months = calculate_month_difference(extract_date(articles[-1].get_attribute('outerHTML')))
                    self.logger.info(f"Checking the month difference of last new in the page: {months}")
                    self.selenium.check_donation_and_close()

                    self.logger.info(f"Total articles scraped so far: {len(articles_list)}")
                except Exception as e:
                    self.logger.error(f"Error while getting news articles: {e}")
                    break
            
            self.process_articles(articles_list)

        except Exception as e:
            # general case expected && unexpected errors
            # if the internet is down or cut off we get unexpected errors, or if the server is down ...
            self.logger.error(f"Error scraping news: {e}")
        finally:
            self.selenium.close()
    
    def get_articles_list(self, articles):
        self.logger.info("Extracting articles information...")
        articles_list = []
        for article in articles:
            article_dict = extract_info(article.get_attribute('outerHTML'))
            articles_list.append(article_dict)
        return articles_list

    def process_articles(self, articles):
        self.logger.info("Processing articles...")
        data = []
        image_urls = []
        for article in articles:
            title = article.get('title')
            date = article.get('date')
            description = article.get("description")
            count_phases = count_phrases(title, description, self.search_phrase)
            contains_money = extract_money(title) or extract_money(description)
            image_url = article.get('image')
            if image_url != '' or image_url != None:
                image_filename = f"{title[:10].strip()}.jpg"
                image_filename = image_filename.replace(" ", "_")
                image_urls.append((image_url, image_filename))
            else:
                image_filename = ''

            data.append({
                'title': title,
                'date': date,
                'description': description,
                'picture_filename': image_filename,
                'count_phrases': count_phases,
                'contains_money': contains_money
            })
        self.logger.info(f"Total articles processed: {len(data)}")
        self.info(f"Total images to download: {len(image_urls)}")
        self.info("Downloading images...")
        save_images_with_threadpoolexecutor(image_urls)
        self.info("Saving data to Excel...")
        save_to_excel(data, f"{self.search_phrase}_news.xlsx")