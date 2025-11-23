import pytest
import time
from unittest.mock import Mock
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from logic_layer import (
    SlugGeneratorService, 
    UrlValidationService, 
    GeoLocationService,
    LinkExpirationService,
    LinkBusinessService
)
from data_layer import InMemoryRepository
from models import LinkData

class TestSlugGeneratorService:
    def test_generate_default_length(self):
        slug = SlugGeneratorService.generate()
        assert len(slug) == 7
        assert slug.isalnum()

    def test_generate_custom_length(self):
        slug = SlugGeneratorService.generate(10)
        assert len(slug) == 10

class TestUrlValidationService:
    def test_google_drive_urls(self):
        valid_urls = [
            'https://drive.google.com/file/d/123/view',
            'https://docs.google.com/document/d/123/edit'
        ]
        for url in valid_urls:
            assert UrlValidationService.is_google_drive_url(url)

    def test_invalid_urls(self):
        invalid_urls = ['https://example.com', 'https://dropbox.com']
        for url in invalid_urls:
            assert not UrlValidationService.is_google_drive_url(url)

    def test_valid_url_format(self):
        assert UrlValidationService.is_valid_url('https://example.com')
        assert UrlValidationService.is_valid_url('http://example.com')
        assert not UrlValidationService.is_valid_url('invalid-url')

class TestLinkExpirationService:
    def test_not_expired(self):
        future_time = int(time.time()) + 3600
        assert not LinkExpirationService.is_expired(future_time)

    def test_expired(self):
        past_time = int(time.time()) - 3600
        assert LinkExpirationService.is_expired(past_time)

    def test_no_expiry(self):
        assert not LinkExpirationService.is_expired(None)

class TestLinkBusinessService:
    def setup_method(self):
        self.repository = InMemoryRepository()
        self.service = LinkBusinessService(self.repository)

    def test_create_short_link_success(self):
        url = 'https://drive.google.com/file/d/123/view'
        result = self.service.create_short_link(url, 24)
        
        assert result.original_url == url
        assert len(result.slug) == 7
        assert result.expires_at is not None

    def test_create_short_link_invalid_url(self):
        with pytest.raises(ValueError, match="Only Google Drive URLs are allowed"):
            self.service.create_short_link('https://example.com')

    def test_get_redirect_url_success(self):
        url = 'https://drive.google.com/file/d/123/view'
        link_data = self.service.create_short_link(url, 24)
        
        redirect_url = self.service.get_redirect_url(link_data.slug, '127.0.0.1', 'Test Agent')
        assert redirect_url == url

    def test_get_redirect_url_not_found(self):
        result = self.service.get_redirect_url('nonexistent', '127.0.0.1', 'Test Agent')
        assert result is None