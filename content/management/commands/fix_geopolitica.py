from django.core.management.base import BaseCommand
from content.models import HomePage, SectionPage


class Command(BaseCommand):
    help = 'Create or fix the Geopolítica section page'

    def handle(self, *args, **options):
        # Check if geopolitica section already exists
        existing = SectionPage.objects.filter(section_key='geopolitica').first()
        
        if existing:
            self.stdout.write(self.style.WARNING(
                f'Geopolítica section already exists: "{existing.title}" at {existing.url}'
            ))
            self.stdout.write('If this is not working correctly, you can:')
            self.stdout.write('1. Delete it from the Wagtail admin')
            self.stdout.write('2. Run this command again to recreate it')
            return
        
        # Check for any page with slug 'geopolitica'
        from wagtail.models import Page
        slug_conflict = Page.objects.filter(slug='geopolitica').first()
        
        if slug_conflict and slug_conflict.specific_class != SectionPage:
            self.stdout.write(self.style.ERROR(
                f'⚠️  Found page with slug "geopolitica" but it is not a SectionPage!'
            ))
            self.stdout.write(f'   Page type: {slug_conflict.specific_class.__name__}')
            self.stdout.write(f'   Title: {slug_conflict.title}')
            self.stdout.write(f'   URL: {slug_conflict.url}')
            self.stdout.write('\nPlease delete or rename this page, then run this command again.')
            return
        
        # Get the HomePage
        try:
            home_page = HomePage.objects.first()
            if not home_page:
                self.stdout.write(self.style.ERROR('No HomePage found! Run setup_site first.'))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error finding HomePage: {str(e)}'))
            return
        
        # Create the Geopolítica section
        try:
            section_page = SectionPage(
                title='Geopolítica',
                slug='geopolitica',
                section_key='geopolitica',
                introduction='Análises sobre política internacional, relações entre nações e conflitos globais'
            )
            home_page.add_child(instance=section_page)
            section_page.save_revision().publish()
            
            self.stdout.write(self.style.SUCCESS(
                f'\n✅ Created Geopolítica section successfully!'
            ))
            self.stdout.write(f'   URL: {section_page.url}')
            self.stdout.write(f'   Page ID: {section_page.id}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error creating Geopolítica section: {str(e)}'))
            self.stdout.write('\nPlease check:')
            self.stdout.write('1. That there is no page with slug "geopolitica"')
            self.stdout.write('2. That there is no SectionPage with section_key "geopolitica"')
            self.stdout.write('3. Database constraints and permissions')
