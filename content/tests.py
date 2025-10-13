from django.test import TestCase
from datetime import datetime, timedelta, date
from django.utils import timezone
import zoneinfo
from content.templatetags.navigation_tags import timesince_brasilia, get_support_sections
from wagtail.models import Site, Page
from content.models import HomePage, SupportSectionPage


class SupportSectionNavigationTestCase(TestCase):
    """Test cases for the support sections navigation"""
    
    def setUp(self):
        """Set up test environment with a home page and support sections"""
        # Get the root page
        root_page = Page.objects.get(id=1)
        
        # Create a home page
        self.home_page = HomePage(
            title="Test Home",
            slug="test-home",
        )
        root_page.add_child(instance=self.home_page)
        
        # Set up a site pointing to the home page
        self.site = Site.objects.create(
            hostname='testserver',
            root_page=self.home_page,
            is_default_site=True,
            site_name='Test Site'
        )
        
        # Create some support section pages
        self.escatologia = SupportSectionPage(
            title="Escatologia",
            slug="escatologia",
            introduction="Seção sobre escatologia",
        )
        self.home_page.add_child(instance=self.escatologia)
        
        self.teologia = SupportSectionPage(
            title="Teologia",
            slug="teologia",
            introduction="Seção sobre teologia",
        )
        self.home_page.add_child(instance=self.teologia)
    
    def test_get_support_sections_returns_all_published(self):
        """Test that get_support_sections returns all published support sections"""
        sections = get_support_sections()
        self.assertEqual(sections.count(), 2)
        
        section_titles = [section.title for section in sections]
        self.assertIn("Escatologia", section_titles)
        self.assertIn("Teologia", section_titles)
    
    def test_support_section_url_has_subsecao_prefix(self):
        """Test that support section URLs have the /subsecao/ prefix"""
        url_parts = self.escatologia.get_url_parts()
        self.assertIsNotNone(url_parts)
        
        site_id, root_url, page_path = url_parts
        self.assertTrue(page_path.startswith('/subsecao/'))
        self.assertIn('escatologia', page_path)


class TimesinceBrasiliaTestCase(TestCase):
    """Test cases for the timesince_brasilia filter"""
    
    def setUp(self):
        self.brasilia_tz = zoneinfo.ZoneInfo('America/Sao_Paulo')
        self.now = timezone.now()
    
    def test_now_returns_agora(self):
        """Test that current time returns 'agora'"""
        result = timesince_brasilia(self.now)
        self.assertEqual(result, 'agora')
    
    def test_minutes_ago(self):
        """Test minutes elapsed display"""
        thirty_min_ago = self.now - timedelta(minutes=30)
        result = timesince_brasilia(thirty_min_ago)
        self.assertEqual(result, '30 minutos')
        
        one_min_ago = self.now - timedelta(minutes=1)
        result = timesince_brasilia(one_min_ago)
        self.assertEqual(result, '1 minuto')
    
    def test_hours_ago(self):
        """Test hours elapsed display - this was the main bug"""
        three_hours_ago = self.now - timedelta(hours=3)
        result = timesince_brasilia(three_hours_ago)
        self.assertEqual(result, '3 horas')
        
        one_hour_ago = self.now - timedelta(hours=1)
        result = timesince_brasilia(one_hour_ago)
        self.assertEqual(result, '1 hora')
    
    def test_days_ago(self):
        """Test days elapsed display"""
        one_day_ago = self.now - timedelta(days=1)
        result = timesince_brasilia(one_day_ago)
        self.assertEqual(result, '1 dia')
        
        three_days_ago = self.now - timedelta(days=3)
        result = timesince_brasilia(three_days_ago)
        self.assertEqual(result, '3 dias')
    
    def test_months_ago(self):
        """Test months elapsed display"""
        forty_days_ago = self.now - timedelta(days=40)
        result = timesince_brasilia(forty_days_ago)
        self.assertEqual(result, '1 mês')
        
        seventy_days_ago = self.now - timedelta(days=70)
        result = timesince_brasilia(seventy_days_ago)
        self.assertEqual(result, '2 meses')
    
    def test_date_object(self):
        """Test that date objects are handled correctly"""
        today = date.today()
        result = timesince_brasilia(today)
        # Should return some time value, not empty
        self.assertIsNotNone(result)
        self.assertNotEqual(result, '')
    
    def test_future_date_returns_agora(self):
        """Test that future dates return 'agora'"""
        future = self.now + timedelta(hours=1)
        result = timesince_brasilia(future)
        self.assertEqual(result, 'agora')
    
    def test_none_returns_empty(self):
        """Test that None returns empty string"""
        result = timesince_brasilia(None)
        self.assertEqual(result, '')
