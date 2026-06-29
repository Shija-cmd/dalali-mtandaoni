from django.core.management.base import BaseCommand

from properties.category_seed import seed_default_categories
from properties.models import Category


class Command(BaseCommand):

    help = 'Populate the default listing categories.'

    def handle(self, *args, **options):

        created_count = seed_default_categories(
            Category,
            self.stdout
        )

        total_count = Category.objects.count()

        self.stdout.write(
            f'Categories created: {created_count}'
        )
        self.stdout.write(
            f'Categories total: {total_count}'
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Category database populated successfully.'
            )
        )
