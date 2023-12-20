from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import cssutils
import pyautogui
import time

def download_images_from_react_website(url, click_position):

    images_folder = 'images'
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    # use Chrome to access web
    driver = webdriver.Chrome()

    try:
        # open the web page in the browser
        driver.get(url)

        # wait for the page to load
        driver.implicitly_wait(10)
        
        # Open the web page
        pyautogui.click(click_position[0], click_position[1])
        time.sleep(2)  # Wait for the page to load (adjust as needed)

        # get html
        html = driver.page_source

        # use BeautifulSoup to parse html
        soup = BeautifulSoup(html, 'html.parser')

        # find all img tags
        img_tags = soup.find_all('img')
        
        # download images specified in img src
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url:
                img_url = urljoin(url, img_url)
                img_name = os.path.basename(urlparse(img_url).path)
                img_path = os.path.join(images_folder, img_name)

                with open(img_path, 'wb') as img_file:
                    img_file.write(requests.get(img_url).content)

                print(f'Downloaded: {img_name}')
        
        # Extract and download images specified in background-image
        background_images  = 'background_images'
        if not os.path.exists(background_images):
            os.makedirs(background_images)
        
        style_tags = soup.find_all('div', class_='swiper-slide')
        
        for style_tag in style_tags:
            style = style_tag.get('style')
            if style:
                style = cssutils.parseStyle(style)
                img_url = style['background-image']
                if img_url:
                    img_url = img_url.replace('url(', '').replace(')', '')
                    img_url = urljoin(url, img_url)
                    img_name = os.path.basename(urlparse(img_url).path)
                    img_path = os.path.join(background_images, img_name)

                    # Download the image
                    with open(img_path, 'wb') as img_file:
                        img_file.write(requests.get(img_url).content)

                    print(f'Downloaded: {img_name}')

    finally:
        driver.quit()

url_to_scrape = 'https://newjeans.kr/'
click_position = (670, 180)
download_images_from_react_website(url_to_scrape, click_position)
