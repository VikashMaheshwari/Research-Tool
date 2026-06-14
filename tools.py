from langchain_core.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup
import requests
from rich import print
import os
import sys
from dotenv import load_dotenv

# Ensure stdout uses UTF-8 to avoid Unicode encoding errors on Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

### tavily 
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily = TavilyClient(api_key=TAVILY_API_KEY)

@tool
def web_search(query:str) -> str:
    """The task of this tool is to search the information based on the query and return the information"""
    result = tavily.search(query=query,max_results=3)
    out = []
    for r in result['results']:
        out.append(f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:150]}")
    return '\n---\n'.join(out)
###print(web_search.invoke("i want the latest  news of june 2026 in AI which has not reached to the mass population or any secrative news"))


### scrapping using the beautifulsoup

@tool
def scrape_url(url: str) -> str:
    """Scrapes the full text content from a given URL using BeautifulSoup and returns the cleaned text."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        lines = [line for line in text.splitlines() if line.strip()]
        return "\n".join(lines)[:1000]

    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"
    except Exception as e:
        return f"Error parsing content: {e}"

###print(scrape_url.invoke("https://federalnewsnetwork.com/commentary/2026/06/the-ai-arms-race-everyones-ignoring/"))

