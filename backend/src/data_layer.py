import json
import os
from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from models import LinkData, ClickLog, Analytics

class LinkRepository(ABC):
    @abstractmethod
    def save_link(self, link_data: LinkData) -> None:
        pass
    
    @abstractmethod
    def get_link(self, slug: str) -> Optional[LinkData]:
        pass
    
    @abstractmethod
    def log_click(self, slug: str, click_log: ClickLog) -> None:
        pass
    
    @abstractmethod
    def get_analytics(self, slug: str) -> Optional[Analytics]:
        pass

class InMemoryRepository(LinkRepository):
    def __init__(self):
        self.links: Dict[str, dict] = {}
        self.analytics: Dict[str, List[dict]] = {}
    
    def save_link(self, link_data: LinkData) -> None:
        self.links[link_data.slug] = {
            'slug': link_data.slug,
            'original_url': link_data.original_url,
            'created_at': link_data.created_at,
            'expires_at': link_data.expires_at,
            'click_count': link_data.click_count
        }
        self.analytics[link_data.slug] = []
    
    def get_link(self, slug: str) -> Optional[LinkData]:
        if slug not in self.links:
            return None
        
        data = self.links[slug]
        return LinkData(
            slug=data['slug'],
            original_url=data['original_url'],
            created_at=data['created_at'],
            expires_at=data['expires_at'],
            click_count=data['click_count']
        )
    
    def log_click(self, slug: str, click_log: ClickLog) -> None:
        if slug in self.analytics:
            self.analytics[slug].append({
                'timestamp': click_log.timestamp,
                'ip': click_log.ip,
                'user_agent': click_log.user_agent,
                'country': click_log.country
            })
            self.links[slug]['click_count'] += 1
    
    def get_analytics(self, slug: str) -> Optional[Analytics]:
        if slug not in self.links:
            return None
        
        click_logs = [
            ClickLog(
                timestamp=log['timestamp'],
                ip=log['ip'],
                user_agent=log['user_agent'],
                country=log['country']
            ) for log in self.analytics.get(slug, [])
        ]
        
        timestamps = [log.timestamp for log in click_logs]
        return Analytics(
            total_clicks=self.links[slug]['click_count'],
            first_click=min(timestamps) if timestamps else None,
            last_click=max(timestamps) if timestamps else None,
            click_logs=click_logs
        )

class FileRepository(LinkRepository):
    def __init__(self, data_file: str = 'linkpulse_data.json'):
        self.data_file = data_file
        self._load_data()
    
    def _load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.links = data.get('links', {})
                self.analytics = data.get('analytics', {})
        else:
            self.links = {}
            self.analytics = {}
    
    def _save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump({
                'links': self.links,
                'analytics': self.analytics
            }, f, indent=2)
    
    def save_link(self, link_data: LinkData) -> None:
        self.links[link_data.slug] = {
            'slug': link_data.slug,
            'original_url': link_data.original_url,
            'created_at': link_data.created_at,
            'expires_at': link_data.expires_at,
            'click_count': link_data.click_count
        }
        self.analytics[link_data.slug] = []
        self._save_data()
    
    def get_link(self, slug: str) -> Optional[LinkData]:
        if slug not in self.links:
            return None
        
        data = self.links[slug]
        return LinkData(
            slug=data['slug'],
            original_url=data['original_url'],
            created_at=data['created_at'],
            expires_at=data['expires_at'],
            click_count=data['click_count']
        )
    
    def log_click(self, slug: str, click_log: ClickLog) -> None:
        if slug in self.analytics:
            self.analytics[slug].append({
                'timestamp': click_log.timestamp,
                'ip': click_log.ip,
                'user_agent': click_log.user_agent,
                'country': click_log.country
            })
            self.links[slug]['click_count'] += 1
            self._save_data()
    
    def get_analytics(self, slug: str) -> Optional[Analytics]:
        if slug not in self.links:
            return None
        
        click_logs = [
            ClickLog(
                timestamp=log['timestamp'],
                ip=log['ip'],
                user_agent=log['user_agent'],
                country=log['country']
            ) for log in self.analytics.get(slug, [])
        ]
        
        timestamps = [log.timestamp for log in click_logs]
        return Analytics(
            total_clicks=self.links[slug]['click_count'],
            first_click=min(timestamps) if timestamps else None,
            last_click=max(timestamps) if timestamps else None,
            click_logs=click_logs
        )