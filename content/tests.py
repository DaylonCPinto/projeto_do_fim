from django.test import TestCase
from datetime import datetime, timedelta, date
from django.utils import timezone
import zoneinfo
from content.templatetags.navigation_tags import timesince_brasilia


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
