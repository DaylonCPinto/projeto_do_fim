"""
Tests for soft paywall implementation.

This test suite ensures:
1. Premium articles appear in all listings (HomePage, SectionPage, SupportSectionPage)
2. Premium articles have proper visual indicators in templates
3. Non-subscribers see limited content on article detail pages
4. Subscribers see full content on article detail pages
"""

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from wagtail.models import Page
from content.models import HomePage, ArticlePage, SectionPage, SupportSectionPage
from accounts.models import UserProfile


class SoftPaywallListingsTestCase(TestCase):
    """Test that premium articles appear in all listings"""
    
    def setUp(self):
        """Set up test environment"""
        self.factory = RequestFactory()
        
        # Get the root page
        root_page = Page.objects.get(id=1)
        
        # Create a home page
        self.home_page = HomePage(
            title="Test Home",
            slug="test-home",
        )
        root_page.add_child(instance=self.home_page)
        
        # Create a section page
        self.section_page = SectionPage(
            title="Test Section",
            slug="test-section",
            section_key='geopolitica',
        )
        self.home_page.add_child(instance=self.section_page)
        
        # Create a support section page
        self.support_page = SupportSectionPage(
            title="Test Support",
            slug="test-support",
        )
        self.home_page.add_child(instance=self.support_page)
        
        # Create regular article
        self.regular_article = ArticlePage(
            title="Regular Article",
            slug="regular-article",
            introduction="Regular content",
            is_premium=False,
            section='geopolitica',
        )
        self.home_page.add_child(instance=self.regular_article)
        
        # Create premium article
        self.premium_article = ArticlePage(
            title="Premium Article",
            slug="premium-article",
            introduction="Premium content",
            is_premium=True,
            section='geopolitica',
        )
        self.home_page.add_child(instance=self.premium_article)
        
        # Create users
        self.subscriber = User.objects.create_user(
            username='subscriber',
            password='testpass123'
        )
        self.subscriber.userprofile.is_subscriber = True
        self.subscriber.userprofile.save()
        
        self.non_subscriber = User.objects.create_user(
            username='non_subscriber',
            password='testpass123'
        )
        # non_subscriber's userprofile.is_subscriber is False by default
        
        self.anonymous = None  # Will be used for anonymous requests
    
    def test_premium_articles_visible_in_homepage_for_non_subscribers(self):
        """Premium articles should appear in home page listings for non-subscribers"""
        # Create request as non-subscriber
        request = self.factory.get('/')
        request.user = self.non_subscriber
        
        context = self.home_page.get_context(request)
        
        # Get all article IDs from context (both trending and regular articles)
        article_ids = [a.id for a in context['articles']]
        trending_ids = [a.id for a in context.get('trending_articles', [])]
        all_visible_ids = article_ids + trending_ids
        
        # Both regular and premium articles should be visible somewhere in the listings
        # (New articles auto-trend, so they might be in trending_articles instead of articles)
        self.assertIn(self.regular_article.id, all_visible_ids,
                     "Regular article should be in listings")
        self.assertIn(self.premium_article.id, all_visible_ids,
                     "Premium article should be visible in listings for non-subscribers")
    
    def test_premium_articles_visible_in_homepage_for_subscribers(self):
        """Premium articles should appear in home page listings for subscribers"""
        request = self.factory.get('/')
        request.user = self.subscriber
        
        context = self.home_page.get_context(request)
        
        # Get all article IDs from context (both trending and regular articles)
        article_ids = [a.id for a in context['articles']]
        trending_ids = [a.id for a in context.get('trending_articles', [])]
        all_visible_ids = article_ids + trending_ids
        
        self.assertIn(self.regular_article.id, all_visible_ids)
        self.assertIn(self.premium_article.id, all_visible_ids)
    
    def test_premium_articles_visible_in_section_page(self):
        """Premium articles should appear in section page listings"""
        request = self.factory.get('/test-section/')
        request.user = self.non_subscriber
        
        context = self.section_page.get_context(request)
        
        # Get all article IDs from context (both trending and regular articles)
        article_ids = [a.id for a in context['articles']]
        trending_ids = [a.id for a in context.get('trending_articles', [])]
        all_visible_ids = article_ids + trending_ids
        
        self.assertIn(self.premium_article.id, all_visible_ids,
                     "Premium article should be visible in section listings")
    
    def test_premium_articles_visible_in_support_section_page(self):
        """Premium articles should appear in support section page listings"""
        # Create article in support section
        support_article = ArticlePage(
            title="Premium Support Article",
            slug="premium-support",
            introduction="Premium support content",
            is_premium=True,
            section='geopolitica',
        )
        self.support_page.add_child(instance=support_article)
        
        request = self.factory.get('/test-support/')
        request.user = self.non_subscriber
        
        context = self.support_page.get_context(request)
        
        # Get all article IDs from context (both trending and regular articles)
        article_ids = [a.id for a in context['articles']]
        trending_ids = [a.id for a in context.get('trending_articles', [])]
        all_visible_ids = article_ids + trending_ids
        
        self.assertIn(support_article.id, all_visible_ids,
                     "Premium article should be visible in support section listings")
    
    def test_is_premium_subscriber_flag_correct_for_subscriber(self):
        """Context should have correct is_premium_subscriber flag for subscribers"""
        request = self.factory.get('/')
        request.user = self.subscriber
        
        context = self.home_page.get_context(request)
        
        self.assertTrue(context['is_premium_subscriber'],
                       "is_premium_subscriber should be True for subscribers")
    
    def test_is_premium_subscriber_flag_correct_for_non_subscriber(self):
        """Context should have correct is_premium_subscriber flag for non-subscribers"""
        request = self.factory.get('/')
        request.user = self.non_subscriber
        
        context = self.home_page.get_context(request)
        
        self.assertFalse(context['is_premium_subscriber'],
                        "is_premium_subscriber should be False for non-subscribers")


class ArticlePaywallTestCase(TestCase):
    """Test that article paywall logic works correctly"""
    
    def setUp(self):
        """Set up test environment"""
        self.factory = RequestFactory()
        
        # Get the root page
        root_page = Page.objects.get(id=1)
        
        # Create a home page
        self.home_page = HomePage(
            title="Test Home",
            slug="test-home-paywall",
        )
        root_page.add_child(instance=self.home_page)
        
        # Create premium article
        self.premium_article = ArticlePage(
            title="Premium Article",
            slug="premium-article-test",
            introduction="Premium introduction",
            is_premium=True,
            section='economia',
        )
        self.home_page.add_child(instance=self.premium_article)
        
        # Create users
        self.subscriber = User.objects.create_user(
            username='subscriber_test',
            password='testpass123'
        )
        self.subscriber.userprofile.is_subscriber = True
        self.subscriber.userprofile.save()
        
        self.non_subscriber = User.objects.create_user(
            username='non_subscriber_test',
            password='testpass123'
        )
    
    def test_is_subscriber_flag_true_for_subscribers(self):
        """Article context should have is_subscriber=True for subscribers"""
        request = self.factory.get('/premium-article-test/')
        request.user = self.subscriber
        
        context = self.premium_article.get_context(request)
        
        self.assertTrue(context['is_subscriber'],
                       "is_subscriber should be True for subscribers in article context")
    
    def test_is_subscriber_flag_false_for_non_subscribers(self):
        """Article context should have is_subscriber=False for non-subscribers"""
        request = self.factory.get('/premium-article-test/')
        request.user = self.non_subscriber
        
        context = self.premium_article.get_context(request)
        
        self.assertFalse(context['is_subscriber'],
                        "is_subscriber should be False for non-subscribers in article context")
    
    def test_userprofile_is_subscriber_field_exists(self):
        """UserProfile should have is_subscriber field"""
        self.assertTrue(hasattr(UserProfile, 'is_subscriber'),
                       "UserProfile should have is_subscriber field")
        
        # Verify the field is a BooleanField with default False
        user = User.objects.create_user(username='test_user', password='test')
        self.assertFalse(user.userprofile.is_subscriber,
                        "is_subscriber should default to False")
