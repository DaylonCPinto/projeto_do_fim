from django.core.management.base import BaseCommand
from content.models import SectionPage, ArticlePage


class Command(BaseCommand):
    help = 'Check existing sections and diagnose issues'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== Checking Existing Sections ===\n'))
        
        # List all SectionPages
        sections = SectionPage.objects.all()
        
        if not sections.exists():
            self.stdout.write(self.style.WARNING('No SectionPages found!'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Found {sections.count()} SectionPages:\n'))
            for section in sections:
                self.stdout.write(f'  - Title: "{section.title}"')
                self.stdout.write(f'    Slug: {section.slug}')
                self.stdout.write(f'    Section Key: {section.section_key}')
                self.stdout.write(f'    URL: {section.url}')
                self.stdout.write(f'    Live: {section.live}')
                
                # Count articles in this section
                article_count = ArticlePage.objects.filter(section=section.section_key).live().count()
                self.stdout.write(f'    Articles: {article_count}\n')
        
        # Check which sections are defined but missing
        expected_sections = ['geopolitica', 'economia', 'clima', 'tecnologia', 'escatologia']
        existing_keys = set(sections.values_list('section_key', flat=True))
        missing_keys = set(expected_sections) - existing_keys
        
        if missing_keys:
            self.stdout.write(self.style.WARNING(f'\n⚠️  Missing sections: {", ".join(missing_keys)}'))
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ All expected sections exist!'))
        
        # Check for duplicate section_keys
        from django.db.models import Count
        duplicates = SectionPage.objects.values('section_key').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        if duplicates.exists():
            self.stdout.write(self.style.ERROR('\n❌ Found duplicate section_keys:'))
            for dup in duplicates:
                self.stdout.write(f'   - {dup["section_key"]}: {dup["count"]} pages')
