import requests
from bs4 import BeautifulSoup

def request_github_trending(url):
    page = requests.get(url)
    return page

def extract(page):
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="js-pjax-container")
#     print(results.prettify())
    row_elements = results.find_all("article", class_="Box-row")
    return row_elements

def transform(html_repos):
    repositories_data = []
    for row_element in html_repos:
        title_element = row_element.find("h1", class_="h3 lh-condensed")
        location_element = row_element.find("svg", class_='octicon octicon-star')
        data = {}
        data  = {'deverloper': title_element.text.strip().split("/")[0].strip(), 
             'repository_name': title_element.text.strip().split("/")[1].strip(),
             'nbr_stars':location_element.parent.text.strip() }
        repositories_data.append(data)
    return repositories_data

def format(repositories_data):
    csv_data = "Developer,Repository Name,Number of Stars"
    csv_data += "\n"
    for data in repositories_data:
        csv_data += ",".join(data.values())
        csv_data += "\n"
    return csv_data

url = "https://github.com/trending"
page = request_github_trending(url)
row_elements = extract(page)
repositories_data = transform(row_elements)
csv_data = format(repositories_data)
print(csv_data)
