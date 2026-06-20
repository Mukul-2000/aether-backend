from google import genai
from google.genai import types
from typing import List, Tuple
from src.core.config import settings

# Initialize the new SDK
# The client automatically handles your AQ... token via the environment variable
client = genai.Client(api_key=settings.GEMINI_API_KEY)

class GeminiService:
    MODEL_NAME = "gemini-2.5-flash" 

    @classmethod
    async def extract_search_urls(cls, query: str) -> List[str]:
        # The new SDK uses 'google_search' tool natively
        response = client.models.generate_content(
            model=cls.MODEL_NAME,
            contents=f"Find top 4 web links and resources matching: '{query}'",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        urls = []
        if response.candidates[0].grounding_metadata and response.candidates[0].grounding_metadata.grounding_chunks:
            for chunk in response.candidates[0].grounding_metadata.grounding_chunks:
                if chunk.web and chunk.web.uri:
                    urls.append(chunk.web.uri)
        return urls[:4]

    @classmethod
    async def synthesize_report(cls, query: str, crawled_data: List[Tuple[str, str]]) -> str:
        context = "\n\n".join([f"URL: {url}\nCONTENT: {text}" for url, text in crawled_data])
        
        response = client.models.generate_content(
            model=cls.MODEL_NAME,
            contents=f"USER OBJECTIVE: '{query}'\n\nCRAWLED DATA:\n{context}\n\nSynthesize a premium Markdown brief."
        )
        return response.text