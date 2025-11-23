import secrets
import string
import time
import requests
from typing import Optional
from abc import ABC, abstractmethod
from models import LinkData, ClickLog, Analytics
from data_layer import LinkRepository

class SlugGeneratorService:
    @staticmethod
    def generate(length: int = 7) -> str:
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))

class UrlValidationService:
    @staticmethod
    def is_google_drive_url(url: str) -> bool:
        allowed_domains = ['drive.google.com', 'docs.google.com']
        return any(domain in url for domain in allowed_domains)
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        return url.startswith(('http://', 'https://'))

class GeoLocationService:
    @staticmethod
    def get_country(ip: str) -> str:
        if ip in ['127.0.0.1', 'localhost', '::1']:
            return 'Local'
        
        try:
            response = requests.get(f'https://ipinfo.io/{ip}/json', timeout=2)
            if response.status_code == 200:
                return response.json().get('country', 'Unknown')
        except:
            pass
        return 'Unknown'

class LinkExpirationService:
    @staticmethod
    def is_expired(expires_at: Optional[int]) -> bool:
        if expires_at is None:
            return False
        return int(time.time()) > expires_at
    
    @staticmethod
    def calculate_expiry(ttl_hours: int) -> int:
        return int(time.time()) + (ttl_hours * 3600)

class LinkBusinessService:
    def __init__(self, repository: LinkRepository):
        self.repository = repository
        self.slug_generator = SlugGeneratorService()
        self.url_validator = UrlValidationService()
        self.geo_service = GeoLocationService()
        self.expiration_service = LinkExpirationService()
    
    def create_short_link(self, original_url: str, ttl_hours: int = 24) -> LinkData:
        # Validate URL format
        if not self.url_validator.is_valid_url(original_url):
            raise ValueError("Invalid URL format")
        
        # Validate Google Drive URL
        if not self.url_validator.is_google_drive_url(original_url):
            raise ValueError("Only Google Drive URLs are allowed")
        
        # Generate unique slug
        slug = self._generate_unique_slug()
        
        # Calculate expiration
        expires_at = self.expiration_service.calculate_expiry(ttl_hours) if ttl_hours > 0 else None
        
        # Create link data
        link_data = LinkData(
            slug=slug,
            original_url=original_url,
            created_at=int(time.time()),
            expires_at=expires_at,
            click_count=0
        )
        
        # Save to repository
        self.repository.save_link(link_data)
        return link_data
    
    def get_redirect_url(self, slug: str, ip: str, user_agent: str) -> Optional[str]:
        # Get link data
        link_data = self.repository.get_link(slug)
        if not link_data:
            return None
        
        # Check expiration
        if self.expiration_service.is_expired(link_data.expires_at):
            return None
        
        # Log click
        country = self.geo_service.get_country(ip)
        click_log = ClickLog(
            timestamp=int(time.time()),
            ip=ip,
            user_agent=user_agent,
            country=country
        )
        
        self.repository.log_click(slug, click_log)
        return link_data.original_url
    
    def get_link_analytics(self, slug: str) -> Optional[Analytics]:
        return self.repository.get_analytics(slug)
    
    def _generate_unique_slug(self, max_attempts: int = 10) -> str:
        for _ in range(max_attempts):
            slug = self.slug_generator.generate()
            if not self.repository.get_link(slug):
                return slug
        raise RuntimeError("Unable to generate unique slug")

class AnalyticsService:
    def __init__(self, repository: LinkRepository):
        self.repository = repository
    
    def get_link_stats(self, slug: str) -> Optional[dict]:
        analytics = self.repository.get_analytics(slug)
        if not analytics:
            return None
        
        return {
            'total_clicks': analytics.total_clicks,
            'first_click': analytics.first_click,
            'last_click': analytics.last_click,
            'unique_countries': len(set(log.country for log in analytics.click_logs)),
            'recent_clicks': analytics.click_logs[-10:] if analytics.click_logs else []
        }
    
    def get_click_trends(self, slug: str) -> Optional[dict]:
        analytics = self.repository.get_analytics(slug)
        if not analytics:
            return None
        
        # Group clicks by hour
        hourly_clicks = {}
        for log in analytics.click_logs:
            hour = log.timestamp // 3600 * 3600
            hourly_clicks[hour] = hourly_clicks.get(hour, 0) + 1
        
        return {
            'hourly_distribution': hourly_clicks,
            'country_distribution': self._get_country_stats(analytics.click_logs)
        }
    
    def _get_country_stats(self, click_logs: list) -> dict:
        country_counts = {}
        for log in click_logs:
            country_counts[log.country] = country_counts.get(log.country, 0) + 1
        return country_counts