from django.core.management.base import BaseCommand
from menu_app.models import Item

class Command(BaseCommand):
    help = 'Seed sample menu items'

    def handle(self, *args, **options):
        items = [
            ('Idly', 'Soft idlies with chutney', 20, 'Breakfast'),
            ('Dosa', 'Crispy masala dosa', 40, 'Breakfast'),
            ('Tea', 'Hot tea', 10, 'Beverage'),
            ('Coffee', 'Filter coffee', 15, 'Beverage'),
            ('Veg Meal', 'Full veg meal', 70, 'Meal'),
        ]
        for name, desc, price, cat in items:
            Item.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'price': price, 'category': cat, 'available': True},
            )
        self.stdout.write(self.style.SUCCESS('Sample menu items created.'))
