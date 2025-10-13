from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from content.models import HomePage, SectionPage, ArticlePage


class Command(BaseCommand):
    help = 'Sets up the initial site structure with HomePage and SectionPages'

    def handle(self, *args, **options):
        # Get the root page
        root = Page.objects.get(id=1)
        
        # Check if HomePage already exists
        home_pages = HomePage.objects.all()
        
        if home_pages.exists():
            home_page = home_pages.first()
            self.stdout.write(self.style.WARNING(f'HomePage already exists: {home_page.title}'))
        else:
            # Check for default welcome page
            default_page = Page.objects.filter(slug='home', depth=2).first()
            
            if default_page and default_page.specific_class != HomePage:
                # Convert the default page to HomePage by creating a new one with same position
                self.stdout.write(self.style.WARNING(f'Found default page: {default_page.title}'))
                
                # Create HomePage as a child of root
                home_page = HomePage(
                    title='Início',
                    slug='home',
                    body='Portal de Análise e Notícias'
                )
                # Use the default page's position by adding before deleting
                root.add_child(instance=home_page)
                home_page.save_revision().publish()
                self.stdout.write(self.style.SUCCESS(f'Created HomePage: {home_page.title}'))
                
                # Delete the old default page
                default_page.delete()
                self.stdout.write(self.style.WARNING(f'Removed default page'))
            else:
                # No default page, just create HomePage
                home_page = HomePage(
                    title='Início',
                    slug='home',
                    body='Portal de Análise e Notícias'
                )
                root.add_child(instance=home_page)
                home_page.save_revision().publish()
                self.stdout.write(self.style.SUCCESS(f'Created HomePage: {home_page.title}'))
            
            # Configure site
            sites = Site.objects.all()
            if sites.exists():
                site = sites.first()
                site.root_page = home_page
                site.site_name = 'Portal de Análise'
                site.is_default_site = True
                site.save()
                self.stdout.write(self.style.SUCCESS(f'Updated site to use HomePage'))
            else:
                site = Site.objects.create(
                    hostname='localhost',
                    port=8000,
                    site_name='Portal de Análise',
                    root_page=home_page,
                    is_default_site=True
                )
                self.stdout.write(self.style.SUCCESS(f'Created new site'))
        
        # Define sections to create
        sections = [
            {'key': 'geopolitica', 'title': 'Geopolítica', 'slug': 'geopolitica', 
             'intro': 'Análises sobre política internacional, relações entre nações e conflitos globais'},
            {'key': 'economia', 'title': 'Economia', 'slug': 'economia',
             'intro': 'Notícias e análises sobre mercados, finanças e economia global'},
            {'key': 'clima', 'title': 'Clima', 'slug': 'clima',
             'intro': 'Mudanças climáticas, sustentabilidade e meio ambiente'},
            {'key': 'tecnologia', 'title': 'Tecnologia', 'slug': 'tecnologia',
             'intro': 'Inovação, tecnologia e transformação digital'},
        ]
        
        # Create section pages
        for section_data in sections:
            # Check if section already exists
            existing_section = SectionPage.objects.filter(section_key=section_data['key']).first()
            
            if existing_section:
                self.stdout.write(self.style.WARNING(
                    f'SectionPage already exists: {existing_section.title} (key={section_data["key"]})'
                ))
            else:
                try:
                    section_page = SectionPage(
                        title=section_data['title'],
                        slug=section_data['slug'],
                        section_key=section_data['key'],
                        introduction=section_data['intro']
                    )
                    home_page.add_child(instance=section_page)
                    section_page.save_revision().publish()
                    self.stdout.write(self.style.SUCCESS(
                        f'Created SectionPage: {section_page.title} ({section_page.url})'
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Error creating SectionPage for {section_data["key"]}: {str(e)}'
                    ))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Site setup complete!'))
        self.stdout.write(self.style.SUCCESS(f'Home page URL: {home_page.url}'))
        self.stdout.write(self.style.SUCCESS('\nSection URLs:'))
        for section in SectionPage.objects.all():
            self.stdout.write(self.style.SUCCESS(f'  - {section.title}: {section.url}'))
