# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

# Intialize the browser, create a data dictionary, end the WebDriver, and return
# scraped data
def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    # Set news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data={
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(broswer):

    # Visit the Mars NASA news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    # This searches for elements with a specific combination of ul and li tags and item_list and slide atts
    # This also tells the browser to wait 1 second before searching so that dynamic pages have time to load
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)

    # Set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Use the parent element to find the first 'a' tag and save it as a 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p

def featured_image(browser):

    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting HTML with Soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        # Find the relative image URL
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use base URL to create absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url


def mars_facts():

    # Add try/except for error handling
    try:


        # Scrape table with a DF
        # Create a new DF from the HTML table. Index of 0 tells Pandas to pull only the first table it encounter
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns to the new DF
    df.columns=['Description', 'Mars']

    # Convert 'Description' column into the index and inplace=True means the updated index will remain in place,
    # without having to reassign the DF to a new variable
    df.set_index('Description', inplace=True)
    df

    # Convert DF back into HTML-ready code
    return df.to_html(classes='table table-striped')

if __name__ == '__main__':

    # If running as a script, print scraped data
    print(scrape_all())