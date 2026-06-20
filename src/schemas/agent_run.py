from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class AgentRunBase(BaseModel):
    user_query: str = Field(..., description="The main execution objective requested from the AI Agent.")
    target_depth: int = Field(3, ge=1, le=10, description="Max analytical search traversal depth limit.")

class AgentRunCreate(AgentRunBase):
    pass

class AgentRunResponse(AgentRunBase):
    id: str = Field(..., description="Unique generated UUID identifier of the research task execution.")
    status: str = Field("queued", description="Current execution state")
    scraped_urls: List[str] = Field(default_factory=list, description="Web links analyzed.")
    final_report: Optional[str] = Field(None, description="The final generated Markdown intelligence brief.")
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }