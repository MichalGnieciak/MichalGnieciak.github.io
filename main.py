import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")

post_title = "Your-favourite-color"

filename = f"{current_date}-{post_title}.md"

posts_folder = "_posts"
file_path = os.path.join(posts_folder, filename)

os.makedirs(posts_folder, exist_ok=True)

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
    
    post_markdown += """
### {}
{}
    """.format(color, desc)

with open(file_path, "w") as markdown_file:
    markdown_file.write(f"---\n")
    markdown_file.write(f"title: {post_title.replace('-', ' ').title()}\n")
    markdown_file.write(f"date: {current_date} 12:00:00\n")
    markdown_file.write(f"categories: [Blogging]\n")
    markdown_file.write(f"tags: [introduction]\n")
    markdown_file.write(f"---\n")
    markdown_file.write("\n")
    markdown_file.write(post_markdown)