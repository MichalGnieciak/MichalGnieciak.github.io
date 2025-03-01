import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from duckduckgo_search import DDGS

url = "https://www.rumblerank.com/post/ranking-a-list-of-popular-or-favorite-colors-on-the-spectrum"

response = requests.get(url)
html = BeautifulSoup(response.text, 'html.parser')

list = html.find_all("ol", {"class": "xD-Fd iRNRX"})
if list:
    items = [li.get_text(strip=True) for li in list[1].find_all("li")]

post_markdown = "# What is your favourite color?\n"
post_markdown += "## And what if this question was asked to the whole world?\n"
post_markdown += "## Here are the results: \n"

images = html.find_all("img")
if images:
    for img in images:
        src = img.get("src", "")
        if src.endswith(".gif"):
            post_markdown += f"![]({src})\n"

for i in items:
    color, desc = i.split(" - ", 1)
    
    # Creating subsites for each color :
    current_date = datetime.now().strftime("%Y-%m-%d")

    post_title = "Learn-about-{}".format(color.lower())

    filename = f"{current_date}-{post_title}.md"

    posts_folder = "_posts"
    file_path = os.path.join(posts_folder, filename)

    os.makedirs(posts_folder, exist_ok=True)

    subsite_markdown = "# {}\n".format(color)
    # Image:
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
    for result in results:
        subsite_markdown += f"![]({result['image']})\n"

    # Text:
    search_query = "color " + color + " description"
    results = DDGS().text(
        keywords=search_query,
        region='wt-wt',
        safesearch='off',
        timelimit='7d',
        max_results=1,
    )
    for result in results:
        subsite_markdown += """
### {}
Read more: {}
    """.format(result['body'], result['href'])
        
    with open(file_path, "w") as markdown_file:
        markdown_file.write(f"---\n")
        markdown_file.write(f"title: {post_title.replace('-', ' ').title()}\n")
        markdown_file.write(f"date: {current_date} 12:00:00\n")
        markdown_file.write(f"categories: [Blogging]\n")
        markdown_file.write(f"tags: [introduction]\n")
        markdown_file.write(f"---\n")
        markdown_file.write("\n")
        markdown_file.write(subsite_markdown)
    
    post_markdown += """
### {}
{}
    """.format(color, desc)

current_date = datetime.now().strftime("%Y-%m-%d")

post_title = "Your-favourite-color"

filename = f"{current_date}-{post_title}.md"

posts_folder = "_posts"
file_path = os.path.join(posts_folder, filename)

os.makedirs(posts_folder, exist_ok=True)


with open(file_path, "w") as markdown_file:
    markdown_file.write(f"---\n")
    markdown_file.write(f"title: {post_title.replace('-', ' ').title()}\n")
    markdown_file.write(f"date: {current_date} 12:00:00\n")
    markdown_file.write(f"categories: [Blogging]\n")
    markdown_file.write(f"tags: [introduction]\n")
    markdown_file.write(f"---\n")
    markdown_file.write("\n")
    markdown_file.write(post_markdown)

