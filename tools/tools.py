from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str) -> str:
    """Searches for LinkedIn or Twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res[0]["url"]


# from langchain.serpapi import SerpAPIWrapper
#
#
# def get_profile_url(text: str) -> str:
#     """Searches for LinkedIn Profile Page."""
#     search = SerpAPIWrapper()
#     res = search.run(f"{text}")
#     return res
