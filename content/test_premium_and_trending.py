"""
Tests for Premium and Trending article features.

This test suite ensures:
1. Premium articles remain premium indefinitely (no auto-expiration)
2. Trending articles expire after 3 hours as expected
3. Premium and trending flags are independent
"""

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from freezegun import freeze_time
from wagtail.models import Page
from content.models import HomePage, ArticlePage


class PremiumArticlePersistenceTestCase(TestCase):
    """Test that premium articles never expire automatically"""
    
    def setUp(self):
        """Set up test environment with a home page"""
        # Get the root page
        root_page = Page.objects.get(id=1)
        
        # Create a home page
        self.home_page = HomePage(
            title="Test Home",
            slug="test-home",
        )
        root_page.add_child(instance=self.home_page)
    
    def test_premium_article_remains_premium_after_creation(self):
        """Test that premium article stays premium immediately after creation"""
        article = ArticlePage(
            title="Premium Test Article",
            slug="premium-test",
            introduction="This is a premium article",
            is_premium=True,
            section='geopolitica',
        )
        self.home_page.add_child(instance=article)
        
        # Refresh from database
        article.refresh_from_db()
        
        self.assertTrue(article.is_premium, "Premium flag should remain True after save")
    
    def test_premium_article_persists_after_3_hours(self):
        """Test that premium articles remain premium after 3 hours (trending expiration time)"""
        # Create premium article
        article = ArticlePage(
            title="Premium Long-term Test",
            slug="premium-longterm",
            introduction="Testing premium persistence",
            is_premium=True,
            section='economia',
        )
        self.home_page.add_child(instance=article)
        article.refresh_from_db()
        
        # Verify it's premium
        self.assertTrue(article.is_premium, "Article should be premium initially")
        
        # Fast forward 3 hours
        with freeze_time(timezone.now() + timedelta(hours=3, minutes=1)):
            article.refresh_from_db()
            self.assertTrue(article.is_premium, "Premium flag should persist after 3 hours")
    
    def test_premium_article_persists_after_4_hours(self):
        """Test that premium articles remain premium after 4+ hours"""
        # Create premium article at a specific time
        initial_time = timezone.now()
        
        with freeze_time(initial_time):
            article = ArticlePage(
                title="Premium 4-Hour Test",
                slug="premium-4hour",
                introduction="Testing 4-hour persistence",
                is_premium=True,
                section='tecnologia',
            )
            self.home_page.add_child(instance=article)
            article.refresh_from_db()
            self.assertTrue(article.is_premium)
        
        # Fast forward 4 hours
        with freeze_time(initial_time + timedelta(hours=4)):
            article.refresh_from_db()
            self.assertTrue(article.is_premium, "Premium flag should persist after 4 hours")
    
    def test_premium_article_persists_after_multiple_saves(self):
        """Test that premium flag persists through multiple save operations"""
        article = ArticlePage(
            title="Premium Multi-Save Test",
            slug="premium-multisave",
            introduction="Testing multiple saves",
            is_premium=True,
            section='clima',
        )
        self.home_page.add_child(instance=article)
        article.refresh_from_db()
        
        # Modify and save multiple times
        article.title = "Updated Title 1"
        article.save()
        article.refresh_from_db()
        self.assertTrue(article.is_premium, "Premium should persist after first update")
        
        article.introduction = "Updated introduction"
        article.save()
        article.refresh_from_db()
        self.assertTrue(article.is_premium, "Premium should persist after second update")
    
    def test_premium_and_trending_are_independent(self):
        """Test that premium and trending flags work independently"""
        initial_time = timezone.now()
        
        with freeze_time(initial_time):
            # Create article that is both premium and trending
            article = ArticlePage(
                title="Premium and Trending",
                slug="premium-trending",
                introduction="Both premium and trending",
                is_premium=True,
                is_trending=True,
                trending_until=initial_time + timedelta(hours=3),
                section='geopolitica',
            )
            self.home_page.add_child(instance=article)
            article.refresh_from_db()
            
            self.assertTrue(article.is_premium)
            self.assertTrue(article.is_currently_trending())
        
        # Fast forward past trending expiration
        with freeze_time(initial_time + timedelta(hours=4)):
            article.refresh_from_db()
            
            # Premium should still be True
            self.assertTrue(article.is_premium, "Premium should persist after trending expires")
            
            # Trending should be expired
            self.assertFalse(article.is_currently_trending(), "Trending should expire after 3 hours")


class TrendingArticleExpirationTestCase(TestCase):
    """Test that trending articles expire correctly after 3 hours"""
    
    def setUp(self):
        """Set up test environment with a home page"""
        root_page = Page.objects.get(id=1)
        self.home_page = HomePage(
            title="Test Home Trending",
            slug="test-home-trending",
        )
        root_page.add_child(instance=self.home_page)
    
    def test_new_article_auto_becomes_trending(self):
        """Test that new published articles automatically become trending"""
        article = ArticlePage(
            title="New Auto-Trending Article",
            slug="new-auto-trending",
            introduction="Should auto-trend",
            section='economia',
        )
        self.home_page.add_child(instance=article)
        article.refresh_from_db()
        
        # Should be trending
        self.assertTrue(article.is_trending, "New article should auto-trend")
        self.assertIsNotNone(article.trending_until, "trending_until should be set")
        self.assertTrue(article.is_currently_trending(), "Should be currently trending")
    
    def test_trending_expires_after_3_hours(self):
        """Test that trending expires after 3 hours"""
        initial_time = timezone.now()
        
        with freeze_time(initial_time):
            article = ArticlePage(
                title="Trending Expiration Test",
                slug="trending-expiration",
                introduction="Testing expiration",
                section='tecnologia',
            )
            self.home_page.add_child(instance=article)
            article.refresh_from_db()
            
            self.assertTrue(article.is_currently_trending())
        
        # Just before 3 hours - should still be trending
        with freeze_time(initial_time + timedelta(hours=2, minutes=59)):
            article.refresh_from_db()
            self.assertTrue(article.is_currently_trending(), "Should still be trending before 3 hours")
        
        # After 3 hours - should not be trending
        with freeze_time(initial_time + timedelta(hours=3, minutes=1)):
            article.refresh_from_db()
            self.assertFalse(article.is_currently_trending(), "Should not be trending after 3 hours")
    
    def test_manual_trending_without_expiration(self):
        """Test that manually set trending without expiration date persists"""
        # Create article first without auto-trending (use draft)
        article = ArticlePage(
            title="Manual Trending No Expiration",
            slug="manual-trending-noexp",
            introduction="Manual trending",
            section='clima',
            live=False,  # Start as draft to avoid auto-trending
        )
        self.home_page.add_child(instance=article)
        article.refresh_from_db()
        
        # Now manually set trending without expiration
        article.is_trending = True
        article.trending_until = None  # No expiration
        article.save(update_fields=['is_trending', 'trending_until'])
        article.refresh_from_db()
        
        # Should be trending indefinitely
        self.assertTrue(article.is_currently_trending())
        
        # Still trending after 10 hours
        with freeze_time(timezone.now() + timedelta(hours=10)):
            article.refresh_from_db()
            self.assertTrue(article.is_currently_trending(), "Manual trending should persist indefinitely")
    
    def test_trending_until_is_respected(self):
        """Test that custom trending_until date is respected"""
        initial_time = timezone.now()
        custom_expiration = initial_time + timedelta(hours=5)
        
        with freeze_time(initial_time):
            # Create as draft first to control trending fields
            article = ArticlePage(
                title="Custom Trending Duration",
                slug="custom-trending",
                introduction="Custom duration",
                section='geopolitica',
                live=False,
            )
            self.home_page.add_child(instance=article)
            article.refresh_from_db()
            
            # Now set custom trending expiration
            article.is_trending = True
            article.trending_until = custom_expiration
            article.save(update_fields=['is_trending', 'trending_until'])
            article.refresh_from_db()
            
            self.assertTrue(article.is_currently_trending())
        
        # Before custom expiration - should be trending
        with freeze_time(initial_time + timedelta(hours=4, minutes=30)):
            article.refresh_from_db()
            self.assertTrue(article.is_currently_trending(), "Should be trending before custom expiration")
        
        # After custom expiration - should not be trending
        with freeze_time(initial_time + timedelta(hours=5, minutes=1)):
            article.refresh_from_db()
            self.assertFalse(article.is_currently_trending(), "Should not be trending after custom expiration")


class ArticleSaveMethodTestCase(TestCase):
    """Test that save method never modifies is_premium"""
    
    def setUp(self):
        """Set up test environment"""
        root_page = Page.objects.get(id=1)
        self.home_page = HomePage(
            title="Test Home Save",
            slug="test-home-save",
        )
        root_page.add_child(instance=self.home_page)
    
    def test_save_only_updates_trending_fields(self):
        """Test that save method only updates is_trending and trending_until"""
        initial_time = timezone.now()
        
        with freeze_time(initial_time):
            # Create article as non-premium
            article = ArticlePage(
                title="Save Method Test",
                slug="save-method-test",
                introduction="Testing save",
                is_premium=False,
                section='economia',
            )
            self.home_page.add_child(instance=article)
            article.refresh_from_db()
            
            # Verify auto-trending happened
            self.assertTrue(article.is_trending)
            self.assertIsNotNone(article.trending_until)
            
            # Verify is_premium was NOT changed
            self.assertFalse(article.is_premium, "is_premium should remain False")
        
        # Now manually set to premium
        article.is_premium = True
        article.save()
        article.refresh_from_db()
        
        # Verify premium persists
        self.assertTrue(article.is_premium, "is_premium should be True after manual update")
        
        # Do another save operation
        article.title = "Updated Title"
        article.save()
        article.refresh_from_db()
        
        # Premium should still be True
        self.assertTrue(article.is_premium, "is_premium should persist through saves")
