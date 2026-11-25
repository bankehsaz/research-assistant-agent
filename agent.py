
import requests

from tools import search_web, extract_content


# ==========================================
# 1. Text Summarization
# ==========================================

def summarize_text(text):
    """
    Summarize a given text using a local Ollama LLM.

    Args:
        text (str): Input text.

    Returns:
        str: A summarized version of the input text.
    """

    # Limit input length
    text = text[:2000]

    prompt = f"""
    Summarize this text in 3 to 5 concise bullet points.
    Focus on the main ideas and important findings.

    Text:
    {text}
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:0.5b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 180
                }
            },
            timeout=180
        )

        response.raise_for_status()

        result = response.json()

        return result["response"].strip()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"Ollama API request failed: {e}"
        ) from e

    except (ValueError, KeyError) as e:
        raise RuntimeError(
            f"Invalid response from Ollama: {e}"
        ) from e


# ==========================================
# 2. Research Workflow
# ==========================================

def research(topic, max_results=5):
    """
    Search the web, extract content, and summarize each source.

    Args:
        topic (str): Research topic.
        max_results (int): Maximum number of search results.

    Returns:
        list: A list of dictionaries containing source information.
    """

    sources = []

    # Step 1: Search the web
    search_results = search_web(
        topic,
        max_results=max_results
    )

    # Step 2: Process each search result
    for result in search_results:

        title = result.get("title", "Untitled")
        url = result.get("href")

        if not url:
            continue

        # Step 3: Extract page content
        content = extract_content(url)

        if not content:
            continue

        # Step 4: Summarize extracted content
        try:
            summary = summarize_text(content)

        except RuntimeError:
            continue

        # Step 5: Store source information
        sources.append({
            "title": title,
            "url": url,
            "summary": summary
        })

    return sources


# ==========================================
# 3. Research Report Generation
# ==========================================

def generate_research_report(topic, sources):
    """
    Generate a research report based on source summaries.

    Args:
        topic (str): Research topic.
        sources (list): List of processed sources.

    Returns:
        str: A research report with source links.
    """

    if not sources:
        return "No sources were successfully processed."

    # Step 1: Prepare source summaries
    source_text = ""

    for i, source in enumerate(sources, start=1):

        source_text += f"""
        Source {i}: {source['title']}

        Summary:
        {source['summary']}

        """

    # Step 2: Create report prompt
    prompt = f"""
    You are a research assistant.

    Write a concise research report about:
    {topic}

    Use only the information provided in the source summaries.

    Structure the report into these sections:
    1. Introduction
    2. Key Findings
    3. Overall Conclusion

    Do not invent facts or unsupported information.

    Source Summaries:
    {source_text}
    """

    # Step 3: Generate report using Ollama
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:0.5b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 300
                }
            },
            timeout=180
        )

        response.raise_for_status()

        result = response.json()

        report = result["response"].strip()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"Report generation failed: {e}"
        ) from e

    except (ValueError, KeyError) as e:
        raise RuntimeError(
            f"Invalid response from Ollama: {e}"
        ) from e

    return report
