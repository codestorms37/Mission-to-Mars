#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


# deactivate jedi to speed autocomplete
get_ipython().run_line_magic('config', 'Completer.use_jedi = False')


# In[2]:


import pandas as pd
# to read html table

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# In[3]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# ## No entendí esto????????
# 
# - With the following line, browser.is_element_present_by_css('div.list_text', wait_time=1), we are accomplishing two things.
#   - One is that we're searching for elements with a specific combination of tag (div) and attribute (list_text). As an example, ul.item_list would be found in HTML as \<ul class="item_list">.
#   - Secondly, we're also telling our browser to wait one second before searching for components. The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.

# In[5]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# - Notice how we've assigned slide_elem as the variable to look for the \<div /> tag and its descendent (the other tags within the \<div /> element)? This is our parent element. This means that this element holds all of the other elements within it, and we'll reference it when we want to filter search results even further. The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag with the class of list_text. CSS works from right to left, such as returning the last item on the list instead of the first. Because of this, when using select_one, the first matching element returned will be a \<li /> element with a class of slide and all nested elements within it.

# In[6]:


slide_elem


# In[7]:


slide_elem.find('div', class_='content_title')


# In[8]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[ ]:





# # Important
# 
# - .find() is used when we want only the first class and attribute we've specified.
# - .find_all() is used when we want to retrieve all of the tags and attributes.

# In[9]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# # 10.3.4 Scrape Mars Data: Featured Image
# 
# ### Featured Images

# In[10]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[11]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[12]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[13]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# - An img tag is nested within this HTML, so we've included it.
# - .get('src') pulls the link to the image.

# In[14]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# # 10.3.5 Scrape Mars Data: Mars Facts

# In[15]:


# Visit URL
url = 'https://galaxyfacts-mars.com/'
browser.visit(url)


# In[16]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df


# In[17]:


df.columns=['description', 'Mars', 'Earth']
df


# In[18]:


df.set_index('description', inplace=True)
df


# In[19]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[20]:


df.to_html()


# In[21]:


# browser.quit()


# # Challenge

# ## D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[35]:


# 1. Use browser to visit the URL 
base_url = 'https://marshemispheres.com/'

browser.visit(base_url)


# In[23]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.


# In[24]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[49]:


# Find the product-section
product_section = img_soup.find('div', id='product-section')
# product_section


# In[50]:


# Find the relative image url
descriptions = product_section.findAll('div', class_='description')
# descriptions


# In[46]:


hemisphere_image_urls=[]
for description in descriptions:
    title = description.find('h3').get_text()
    
    page_url = description.find('a').get('href')
    # print(title,page_url)
    
    browser.visit(f"{base_url}{page_url}")
    browser.is_element_present_by_css('div.downloads', wait_time=1)
    
    # Parse the resulting html with soup
    html = browser.html
    page_soup = soup(html, 'html.parser')
    downloads = page_soup.find('div',class_='downloads')
    sample_url = downloads.find('a').get('href')
    # print(sample_url)
    
    sample_full_url = f"{base_url}{sample_url}"
    
    hemisphere_image_urls.append({'img_url': sample_full_url, 'title': title})
    # print(hemisphere_image_urls)


# In[47]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[48]:


# 5. Quit the browser
browser.quit()


# In[ ]:




