from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def get_soup_content(url):
	exe_path = {"executable_path": "chromedriver"}

	with Browser("chrome", **exe_path, headless=True) as browser:
		browser.visit(url)
		content = browser.html
		return BeautifulSoup(content, 'html.parser')

    
def memoized(value, storage):
	if value not in storage:
		storage[value] = value
		return storage[value]
	return ''


def scrape():
	# Get the title and description of top news.
	# Scrape the content:
	news_content = get_soup_content("https://mars.nasa.gov/news/")
	# Data Wrangling:
	content = news_content.find_all(class_="list_text")
	news_title = [element.find(class_="content_title").get_text() for element in content if element.find(class_="content_title")]
	news_p = [element.find(class_="article_teaser_body").get_text() for element in content if element.find(class_="article_teaser_body")]
	news_dic = [{"news_title": key, "news_p": value} for (key, value) in list(zip(news_title, news_p))]

	# Get the featured image from JPL.
	jpl_content = get_soup_content("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
	featured_image_url = "https://www.jpl.nasa.gov{}".format(jpl_content.find(class_="carousel_item")["style"].split(":")[1].split("'")[1])

	# Get the latest tweet of Mars' weather.
	tweet_content = get_soup_content("https://twitter.com/marswxreport?lang=en")
	tweet_mars_weather = tweet_content.find_all(class_="TweetTextSize")[1].get_text()

	# Get the Mars' facts table.
	# Scrape the content:
	facts_content = get_soup_content("http://space-facts.com/mars/")
	# Data Wrangling:
	facts_table = facts_content.find(id="tablepress-mars")
	facts_columns = [title.get_text() for title in facts_table.find_all("td", attrs={"class": "column-1"})]
	facts = [description.get_text() for description in facts_table.find_all("td", attrs={"class": "column-2"})]
	facts_pd = pd.DataFrame([facts], columns =facts_columns)

	# Get the Mars' Hemisphere content.
	# Initialize variables:
	storage = {}
	wide_image_list = []
	base_url = "https://astrogeology.usgs.gov{}"

	# Scrape the content:
	hemis_content = get_soup_content("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
	
	# Data Wrangling:
	html_hemis = hemis_content.find_all(class_="itemLink")
	url_list = [base_url.format(link["href"]) for link in html_hemis if memoized(link["href"], storage)]
	for url in url_list:
		# Scrape the content:
		hemis_image_wide = get_soup_content(url)
		# Get content:
		wide_image_list.append(base_url.format(hemis_image_wide.find(class_="wide-image")["src"]))

	title_list = [title.get_text() for title in hemis_content.find_all("h3")]

	hemis_dic = [{"title": key, "img_url": value} for (key, value) in list(zip(title_list, wide_image_list))]

	return {
		"news_dic": news_dic,
		"featured_image_url": featured_image_url,
		"tweet_mars_weather": tweet_mars_weather,
		"facts_pd": facts_pd.T.to_dict()[0],
		"hemis_dic": hemis_dic
	}
