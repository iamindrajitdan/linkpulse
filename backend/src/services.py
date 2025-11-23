import secrets
import string
import time
import requests
from typing import Optional
from models import LinkData, ClickLog, Analytics

class SlugGenerator:
    @staticmethod
    def generate(length: int = 7) -> str:
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))

class UrlValidator:
    @staticmethod
    def is_google_drive_url(url: str) -> bool:
        return 'drive.google.com' in url or 'docs.google.com' in url

class GeoService:
    @staticmethod
    def get_country(ip: str) -> str:
        try:
            response = requests.get(f'https://ipinfo.io/{ip}/json', timeout=2)
            return response.json().get('country', 'Unknown')
        except:
            return 'Unknown'

class LinkService:
    def __init__(self, repository):
        self.repository = repository
        self.slug_generator = SlugGenerator()
        self.url_validator = UrlValidator()
        self.geo_service = GeoService()

    def create_short_link(self, original_url: str, ttl_hours: int = 24) -> LinkData:
        if not self.url_validator.is_google_drive_url(original_url):
            raise ValueError("Only Google Drive URLs are allowed")
        
        slug = self.slug_generator.generate()
        while self.repository.get_link(slug):
            slug = self.slug_generator.generate()
        
        expires_at = int(time.time()) + (ttl_hours * 3600) if ttl_hours else None
        link_data = LinkData(
            slug=slug,
            original_url=original_url,
            created_at=int(time.time()),
            expires_at=expires_at
        )
        
        self.repository.save_link(link_data)
        return link_data

    def get_redirect_url(self, slug: str, ip: str, user_agent: str) -> Optional[str]:
        link_data = self.repository.get_link(slug)
        if not link_data:
            return None
        
        if link_data.expires_at and int(time.time()) > link_data.expires_at:
            return None
        
        country = self.geo_service.get_country(ip)
        click_log = ClickLog(
            timestamp=int(time.time()),
            ip=ip,
            user_agent=user_agent,
            country=country
        )
        
        self.repository.log_click(slug, click_log)
        return link_data.original_url

    def get_analytics(self, slug: str) -> Optional[Analytics]:
        return self.repository.get_analytics(slug)