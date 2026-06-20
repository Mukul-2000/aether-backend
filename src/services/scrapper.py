import httpx
from bs4 import BeautifulSoup
import re
from typing import Optional

class ScraperService:
    """
    Asynchronous web ingestion service specializing in stripping raw text structures 
    from web target endpoints while filtering headers, navigations, and script bloat.
    """
    
    # Common user agent to prevent request blockage on standard public sites
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

    @classmethod
    async def scrape_url(cls, url: str) -> Optional[str]:
        """
        Asynchronously fetches HTML page content, parses the core article container text,
        and sanitizes it to return a clean unstructured string.
        """
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            try:
                response = await client.get(url, headers=cls.HEADERS)
                if response.status_code != 200:
                    return None
                
                # Load raw HTML into BeautifulSoup structures
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Strip out noisy script nodes, styles, headers, footers and advertisements
                for element in soup(["script", "style", "nav", "footer", "header", "noscript", "aside"]):
                    element.decompose()
                
                # Fetch text components representing the page
                raw_text = soup.get_text(separator="\n")
                
                # Clear redundant newline blocks and formatting garbage
                clean_lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
                clean_content = " ".join(clean_lines)
                
                # Limit return length to prevent LLM context-window overflow during processing
                return clean_content[:8000] if len(clean_content) > 8000 else clean_content
                
            except Exception as e:
                # Silently catch scraping exceptions to maintain non-blocking pipeline loops
                return None