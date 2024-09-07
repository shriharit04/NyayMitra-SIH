import requests
from bs4 import BeautifulSoup

def LinkScraper(search_text):
    """
    Scrapes article titles and links from Indian Kanoon based on search keywords.

    Args:
        search_text (str): The search keywords used to query Indian Kanoon.

    Returns:
        dict: A dictionary with article titles as keys and their corresponding URLs as values.
    """
    # Strip whitespace and replace spaces with "+" for URL encoding
    search_text = search_text.strip().replace(" ", "+")
    search_url = f"https://indiankanoon.org/search/?formInput={search_text}"
    
    # Make the request to the search URL
    response = requests.get(search_url)
    response.raise_for_status()  # Check if the request was successful
    
    # Parse the HTML response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Select the first 10 article links
    links = soup.select('.result_title a')[:10]  
    articles = {}

    # Extract titles and URLs
    for link in links:
        title = link.get_text(strip=True)
        url = "https://indiankanoon.org" + link['href']
        articles[title] = url
    
    return articles

def ExtractArticleContent(url):
    """
    Extracts the content of a given article from its URL.

    Args:
        url (str): The URL of the article to scrape.

    Returns:
        str: The content of the article as a single string.
    """
    # Make the request to the article URL
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    
    # Parse the HTML response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <div> with class 'fragment' and extract all <p> elements
    div_fragment = soup.find('div', class_='fragment')
    if div_fragment is None:
        return ""  # Return an empty string if the fragment is not found
    
    paragraphs = div_fragment.find_all('p')
    content = "\n".join([p.get_text(strip=True) for p in paragraphs])
    
    return content

def ExtractArticleContents(articles):
    """
    Extracts and writes the content of each article to a file.

    Args:
        articles (dict): A dictionary with article titles as keys and their URLs as values.
    """
    contents = []
    error_count = 0

    # Iterate over the articles to extract their content
    for article_title, article_link in articles.items():
        try:
            content = ExtractArticleContent(article_link)
            if content:  # Only append if content is not empty
                contents.append(content)
        except Exception as e:
            error_count += 1
            print(f"Error scraping {article_title}: {e}")
    
    print("Error count:", error_count)
    print("Total articles scraped:", len(contents))

    # Write all the contents to a file
    # with open("scraped_articles.txt", "w") as f:
    #     f.write("\n\n".join(contents))

if __name__ == "__main__":
    search_text = "suit for partition and court fee"
    articles = LinkScraper(search_text)
    ExtractArticleContents(articles)
