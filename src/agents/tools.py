import logging
from typing import List, Dict, Any, Optional
from src.services.scrapper import ScraperService
from src.services.gemini import GeminiService

logger = logging.getLogger("aether.tools")

class AgentTools:
    """
    Central repository of functional capabilities (Tools) exposed to the AetherAgent loop.
    Each tool is strictly typed and documented so LLM models can parse and execute them.
    """

    @staticmethod
    async def web_search_tool(query: str) -> List[str]:
        """
        Executes a live search query utilizing Google Search Grounding metadata 
        to discover the absolute best references, documentations, and emerging trends.
        
        Args:
            query (str): The search terms or research question to search for.
            
        Returns:
            List[str]: A list of discovered target URLs matching the query parameters.
        """
        logger.info(f"🔧 Tool Invoked [web_search_tool] with query: '{query}'")
        try:
            urls = await GeminiService.extract_search_urls(query)
            logger.info(f"✅ [web_search_tool] discovered {len(urls)} target resources.")
            return urls
        except Exception as e:
            logger.error(f"❌ [web_search_tool] failed: {str(e)}")
            return []

    @staticmethod
    async def web_scrape_tool(url: str) -> Optional[str]:
        """
        Connects to a specific URL, bypasses basic anti-bot structures, parses HTML elements,
        strips navigation bloat, and returns the sanitized unstructured text content.
        
        Args:
            url (str): The target website URL to ingest.
            
        Returns:
            Optional[str]: Cleaned raw text representation of the webpage (truncated up to 8000 chars).
        """
        logger.info(f"🔧 Tool Invoked [web_scrape_tool] with URL: '{url}'")
        try:
            content = await ScraperService.scrape_url(url)
            if content:
                logger.info(f"✅ [web_scrape_tool] successfully ingested {len(content)} characters.")
                return content
            logger.warning(f"⚠️ [web_scrape_tool] returned an empty payload for: {url}")
            return None
        except Exception as e:
            logger.error(f"❌ [web_scrape_tool] failed: {str(e)}")
            return None

    @classmethod
    def get_tool_definitions(cls) -> List[Dict[str, Any]]:
        """
        Returns the Gemini-compliant Function Declaration schemas.
        These schemas describe our tools to the Gemini API so it knows how to invoke them.
        """
        return [
            {
                "name": "web_search_tool",
                "description": (
                    "Search the web for up-to-date documentation, alternatives, benchmarks, "
                    "or market trends. Always use this to discover relevant reference links."
                ),
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "query": {
                            "type": "STRING",
                            "description": "Specific search terms or target questions to execute."
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "web_scrape_tool",
                "description": (
                    "Ingests, sanitizes, and extracts the raw main body text of a specific web URL. "
                    "Use this to deep-dive into documentation pages discovered via the search tool."
                ),
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "url": {
                            "type": "STRING",
                            "description": "The exact target URL link to crawl."
                        }
                    },
                    "required": ["url"]
                }
            }
        ]