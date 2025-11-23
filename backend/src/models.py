from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class LinkData:
    slug: str
    original_url: str
    created_at: int
    expires_at: Optional[int]
    click_count: int = 0

@dataclass
class ClickLog:
    timestamp: int
    ip: str
    user_agent: str
    country: str

@dataclass
class Analytics:
    total_clicks: int
    first_click: Optional[int]
    last_click: Optional[int]
    click_logs: List[ClickLog]