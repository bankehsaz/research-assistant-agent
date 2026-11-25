
import trafilatura

from ddgs import DDGS
from urllib.parse import urlparse


# ==========================================
# 1. Web Search
# ==========================================

def search_web(query, max_results=5):
    """
    Search the web and return non-advertising results.

    Args:
        query (str): Search query.
        max_results (int): Maximum number of search results.

    Returns:
        list: A list of search result dictionaries.
    """
    
    # Fetch extra results to compensate for filtered links and ensure enough valid results.
    try:
        raw_results = DDGS().text(
            query,
            max_results=max_results * 3,
            backend="bing"
        )

        results = []

        for result in raw_results:

            url = result.get("href", "")

            parsed_url = urlparse(url)

            # Skip Bing advertising redirect links
            if (
                parsed_url.netloc.lower().endswith("bing.com")
                and parsed_url.path.lower().startswith("/aclick")
            ):
                continue

            results.append(result)

            if len(results) >= max_results:
                break

        return results

    except Exception as e:
        raise RuntimeError(
            f"Web search failed: {e}"
        ) from e


# ==========================================
# 2. Content Extraction
# ==========================================

def extract_content(url):
    """
    Extract the main text content from a web page.

    Args:
        url (str): URL of the web page.

    Returns:
        str or None: Extracted text, or None if extraction fails.
    """

    try:
        downloaded = trafilatura.fetch_url(url)

        if downloaded is None:
            return None

        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=True
        )

        return text

    except Exception:
        return None
