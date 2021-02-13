# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import requests

# Set the exe path and initialize Chrome in Splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

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
slide_elem = news_soup.select_one('ul.item_list li.slide')

# Scraping
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first 'a' tag and save it as a 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting HTML with Soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image URL
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use base URL to create absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

# Scrape table with a DF
# Create a new DF from the HTML table. Index of 0 tells Pandas to pull only the first table it encounter
df = pd.read_html('http://space-facts.com/mars/')[0]

# Assign columns to the new DF
df.columns=['description', 'value']

# Convert 'Description' column into the index and inplace=True means the updated index will remain in place,
# without having to reassign the DF to a new variable
df.set_index('description', inplace=True)
df

# Convert DF back into HTML-ready code
df.to_html()

# 1. Use browser to visit the URL 
usgs_url = 'https://astrogeology.usgs.gov'
hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(hemispheres_url)

hemispheres_html = browser.html

hemispheres_soup = soup(hemispheres_html, 'html.parser')

# 2. Create a list to hold the images and titles.
all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in mars_hemispheres:
    # Collect Title
    hemisphere = i.find('div', class_="description")
    title = hemisphere.h3.text
    
    # Collect image link by browsing to hemisphere page
    hemisphere_link = hemisphere.a["href"]    
    browser.visit(usgs_url + hemisphere_link)
    
    image_html = browser.html
    image_soup = soup(image_html, 'html.parser')
    
    image_link = image_soup.find('div', class_='downloads')
    image_url = image_link.find('li').a['href']

    # Create Dictionary to store title and url info
    image_dict = {}
    image_dict['title'] = title
    image_dict['img_url'] = image_url
    
    hemisphere_image_urls.append(image_dict)

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# Close down automated browser
browser.quit()

