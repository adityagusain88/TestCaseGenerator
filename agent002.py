import os

from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()

tavily_client=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
result=tavily_client.search(query="what is the current weather in delhi India?",max_results=1)
print(result["results"][0])