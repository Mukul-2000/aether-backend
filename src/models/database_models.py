import datetime
import json
from sqlalchemy import Column, String, Integer, DateTime, Text
from src.core.database import Base

class AgentRun(Base):
    """
    SQLAlchemy Database model mapping autonomous agent execution states to SQLite storage.
    """
    __tablename__ = "agent_runs"

    id = Column(String, primary_key=True, index=True)
    user_query = Column(String, nullable=False)
    target_depth = Column(Integer, default=3)
    status = Column(String, default="queued") # queued, crawling, synthesizing, finished, failed
    scraped_urls_json = Column(Text, default="[]") # JSON stringified list of analyzed links
    final_report = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    @property
    def scraped_urls(self) -> list:
        try:
            return json.loads(self.scraped_urls_json or "[]")
        except Exception:
            return []

    @scraped_urls.setter
    def scraped_urls(self, value: list):
        self.scraped_urls_json = json.dumps(value or [])