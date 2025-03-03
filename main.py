# Importing all modules
import requests # For scraping websites
from bs4 import BeautifulSoup   # For data parsing
import os   # For saving files and directories
from datetime import datetime   # For current dates automatically selected
from duckduckgo_search import DDGS  # For automatic web searches

# Providing a URL for webstite from which list will be scraped
url = "https://www.rumblerank.com/post/ranking-a-list-of-popular-or-favorite-colors-on-the-spectrum"

# Scraping the webstie for the list
response = requests.get(url)
html = BeautifulSoup(response.text, 'html.parser')

# Finding the list
list = html.find_all("ol", {"class": "xD-Fd iRNRX"})
if list:
    # Since there are two lists on the page we select the one of interest
    # First one: USA, Secend one: Global
    items = [li.get_text(strip=True) for li in list[1].find_all("li")]

# Creating markdown file body
post_markdown = "# What is your favourite color?\n"
post_markdown += "## And what if this question was asked to the whole world?\n"
post_markdown += "## Here are the results: \n"

# Looking for and image for the list markdown site
images = html.find_all("img")
if images:
    for img in images:
        src = img.get("src", "")
        if src.endswith(".gif"):
            post_markdown += f"![]({src})\n"

# Iterating through each item of the list (colors)
for i in items:
    # Parsing color and it's description from the website
    color, desc = i.split(" - ", 1)
    
    # Creating subsites for each color :
    # Preparing info
    current_date = datetime.now().strftime("%Y-%m-%d")
    post_title = "Learn-about-{}".format(color.lower())
    filename = f"{current_date}-{post_title}.md"
    posts_folder = "_posts"
    file_path = os.path.join(posts_folder, filename)
    os.makedirs(posts_folder, exist_ok=True)

    # Creating a website title - color name
    subsite_markdown = "# {}\n".format(color)
    # Image via web search (duckduckgo_search):
    search_query = "color " + color
    results = DDGS().images(
        keywords=search_query,
        region='wt-wt',
        safesearch='off',
        size=None,
        color=None,
        type_image=None,
        layout=None,
        license_image=None,
        max_results=1,
    )
    # Selecting and adding the image to markdown file
    for result in results:
        subsite_markdown += f"![]({result['image']})\n"

    # Text via web search (duckduckgo_search):
    search_query = "color " + color + " description"
    results = DDGS().text(
        keywords=search_query,
        region='wt-wt',
        safesearch='off',
        timelimit='7d',
        max_results=1,
    )
    # Selecting and adding the description and link for a result found to markdown file
    for result in results:
        subsite_markdown += """
### {}
[Read more]({})
    """.format(result['body'], result['href'])
    
    # Creating the subsite for list element
    with open(file_path, "w") as markdown_file:
        # Chirpy-theme base post file scheme
        markdown_file.write(f"---\n")
        markdown_file.write(f"title: {post_title.replace('-', ' ').title()}\n")
        markdown_file.write(f"date: {current_date} 12:00:00\n")
        markdown_file.write(f"categories: [Color]\n")
        markdown_file.write(f"tags: [learning]\n")
        markdown_file.write(f"---\n")
        markdown_file.write("\n")
        # Content
        markdown_file.write(subsite_markdown)

    # Adding info abot list element to the page with the list
    post_markdown += """
### {}
{}\n
[Learn about {}]({}) 
    """.format(color, desc, color.lower(), f"https://michalgnieciak.github.io/posts/{post_title}/")


# Preapring the list markdown file
current_date = datetime.now().strftime("%Y-%m-%d")
post_title = "Your-favourite-color"
filename = f"{current_date}-{post_title}.md"
posts_folder = "_posts"
file_path = os.path.join(posts_folder, filename)
os.makedirs(posts_folder, exist_ok=True)


with open(file_path, "w") as markdown_file:
    # Chirpy-theme base post file scheme
    markdown_file.write(f"---\n")
    markdown_file.write(f"title: {post_title.replace('-', ' ').title()}\n")
    markdown_file.write(f"date: {current_date} 12:00:00\n")
    markdown_file.write(f"categories: [Explanation]\n")
    markdown_file.write(f"tags: [introduction]\n")
    markdown_file.write(f"---\n")
    markdown_file.write("\n")
    # Content
    markdown_file.write(post_markdown)

