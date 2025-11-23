import pytest
from unittest.mock import Mock
from src.services import SlugGenerator, UrlValidator, LinkService
from src.models import LinkData

class TestSlugGenerator:
    def test_generate_default_length(self):
        slug = SlugGenerator.generate()
        assert len(slug) == 7
        assert slug.isalnum()

    def test_generate_custom_length(self):
        slug = SlugGenerator.generate(10)
        assert len(slug) == 10

class TestUrlValidator:
    def test_valid_google_drive_urls(self):
        valid_urls = [
            'https://drive.google.com/file/d/1234/view',
            'https://docs.google.com/document/d/1234/edit'
        ]
        for url in valid_urls:
            assert UrlValidator.is_google_drive_url(url)

    def test_invalid_urls(self):
        invalid_urls = [
            'https://example.com',
            'https://dropbox.com/file'
        ]
        for url in invalid_urls:
            assert not UrlValidator.is_google_drive_url(url)

class TestLinkService:
    def test_create_short_link_success(self):
        mock_repo = Mock()
        mock_repo.get_link.return_value = None
        
        service = LinkService(mock_repo)
        result = service.create_short_link('https://drive.google.com/file/d/1234/view')
        
        assert result.original_url == 'https://drive.google.com/file/d/1234/view'
        assert len(result.slug) == 7
        mock_repo.save_link.assert_called_once()

    def test_create_short_link_invalid_url(self):
        mock_repo = Mock()
        service = LinkService(mock_repo)
        
        with pytest.raises(ValueError):
            service.create_short_link('https://example.com')