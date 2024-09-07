import requests
from bs4 import BeautifulSoup

def LinkScraper(search_text): 
    '''Scrapes Article Titles and Links to articles if search keywords are given'''

    search_text = "suit for partition and court fee"
    search_text = search_text.strip().replace(" ", "+")
    search_url = f"https://indiankanoon.org/search/?formInput={search_text}"
    # print(search_url)

    # Make the request
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.select('.result_title a')[:10]  
    articles = {}
    # Extract titles and URLs
    for link in links:
        title = link.get_text(strip=True)
        url = "https://indiankanoon.org" + link['href']
        articles[title] = url
    
    return articles

def ExtractArticleContent(url):
    '''Extracts the content of a given article URL'''
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    div_fragment = soup.find('div', class_='fragment')
    paragraphs = div_fragment.find_all('p')
    content = "\n".join([p.get_text(strip=True) for p in paragraphs])
    return content


def ExtractArticleContents(articles):
    contents = []
    errorCount = 0
    for article_title, article_link in articles.items():
        try:
            data = (ExtractArticleContent(article_link))
            contents.append(data)
        except:
            errorCount+=1
            pass
    print("Error : ",errorCount)
    print("Total Scraped" , len(articles))

    #writing to file
    with open("delLater.txt","w") as f:
        f.write("\n\n".join(contents))








# %%
