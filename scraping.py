# Imports

import re
import pandas as pd
# to read html table

import datetime as dt

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# --------------------


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph, news_image = mars_news(browser)
    img_url, img_title = featured_image(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "news_image": news_image,
        "featured_image": img_url,
        "featured_image_title": img_title,
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": full_res_images(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# --------------------

# Scrape Mars News


def mars_news(browser):

    # Scrape Mars News

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        news_section = news_soup.find('div', id='news')
        myRow = news_section.find('div', class_="row")
        myimage = myRow.find('img').get('src')
        # slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        # news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title = myRow.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        # news_p = slide_elem.find(
        #    'div', class_='article_teaser_body').get_text()
        news_p = myRow.find(
            'div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None, None

    return news_title, news_p, myimage

# --------------------


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_title = img_soup.find('h1', class_='media_feature_title').get_text()
    except AttributeError:
        return None, None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url, img_title

# --------------------


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# --------------------


def full_res_images(browser):

    # 1. Use browser to visit the URL
    base_url = 'https://marshemispheres.com/'
    browser.visit(base_url)

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:

        # Find the product-section
        product_section = img_soup.find('div', id='product-section')

        # Find the relative image url
        descriptions = product_section.findAll('div', class_='description')

        hemisphere_image_urls = []
        for description in descriptions:
            title = description.find('h3').get_text()

            page_url = description.find('a').get('href')
            # print(title,page_url)

            browser.visit(f"{base_url}{page_url}")
            browser.is_element_present_by_css('div.downloads', wait_time=1)

            # Parse the resulting html with soup
            html = browser.html
            page_soup = soup(html, 'html.parser')
            downloads = page_soup.find('div', class_='downloads')
            sample_url = downloads.find('a').get('href')
            # print(sample_url)

            sample_full_url = f"{base_url}{sample_url}"

            hemisphere_image_urls.append(
                {'img_url': sample_full_url, 'title': title})
            # print(hemisphere_image_urls)

    except BaseException:
        return [None]

    return hemisphere_image_urls


# --------------------
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
