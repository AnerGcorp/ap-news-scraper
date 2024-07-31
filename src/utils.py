import os
import re
import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from pathlib import Path
from config.config import Config


def extract_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Title
    try:
        title_element = soup.find('div', class_='PagePromo-title')
        title = title_element.find('span', class_='PagePromoContentIcons-text')
        title = title.text.strip() if title else None
    except AttributeError as e:
        title = ''

    # Description
    try:
        desc_element = soup.find('div', class_='PagePromo-description')
        description = desc_element.find('span', class_='PagePromoContentIcons-text')
        if description:
            description = description.text.strip() if description else None
        else:
            description = ''
    except AttributeError as e:
        description = ''

    # Date
    date_iso = extract_date(html_content)

    # Picture
    try:
        picture_element = soup.find('img', class_='Image')
        picture_url = picture_element['src'] if picture_element else ''
    except AttributeError as e:
        picture_url = ''
        
    return {
        'title': title,
        'description': description,
        'date': date_iso,
        'image': picture_url
    }

def extract_date(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Date (timestamp conversion)
    try:
        date_element = soup.find('div', class_='PagePromo-date')
        timestamp = date_element.find('bsp-timestamp')
        if timestamp:
            timestamp = int(timestamp['data-timestamp']) / 1000  # Convert from milliseconds to seconds
            date_iso = datetime.fromtimestamp(timestamp).isoformat()
        else:
            date_iso = datetime.now().isoformat()
    except AttributeError as e:
        date_iso = datetime.now().isoformat()
    
    return date_iso

def count_phrases(title: str | None, description: str | None, search_phrase: str) -> int:
    if title and description:
        return title.count(search_phrase) + description.count(search_phrase)
    elif title:
        return title.count(search_phrase)
    elif description:
        return description.count(search_phrase)
    return 0

def calculate_month_difference(date_string: str) -> int:
    # Convert the date string to a datetime object
    date_obj = datetime.fromisoformat(date_string)

    # Get the current date
    current_date = datetime.now()

    # Calculate the difference in years and months
    years_diff = current_date.year - date_obj.year
    months_diff = current_date.month - date_obj.month

    # Adjust for days if necessary
    if current_date.day < date_obj.day:
        months_diff -= 1
    years_diff -= 1 if months_diff < 0 else 0

    # Calculate total months
    total_months = years_diff * 12 + months_diff

    return total_months

def extract_money(string):
    pattern = re.compile(r'(\$\d+(\.\d{1,2})?)|(\d+ dollars)|(\d+ USD)')
    return bool(pattern.search(string))

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    output_path = os.path.join(Config.OUTPUT_DIR, filename)
    df.to_excel(output_path, index=False)

def save_image(url, filename):
    if url == None or url == '':
        return
    
    # Ensure output directory and subdirectory 'images' exist
    output_path = os.path.join(Config.OUTPUT_DIR, "images")
    Path(output_path).mkdir(parents=True, exist_ok=True)

    response = requests.get(url)
    image_path = os.path.join(output_path, filename)
    with open(image_path, 'wb') as f:
        f.write(response.content)

def save_images_with_threadpoolexecutor(image_urls, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for (url, filename) in image_urls:
            future = executor.submit(save_image, url, filename)
            futures.append(future)

        for future in futures:
            future.result()  # Wait for the task to complete

def elapsed_time(start_time, end_time):
    elapsed_time = end_time - start_time
    return elapsed_time