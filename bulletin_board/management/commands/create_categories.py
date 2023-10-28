from django.core.management import BaseCommand

from bulletin_board.models import AnnouncementCategory


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create announcements categories")

        categories_names = [
            "Танки",
            "Хилы",
            "ДД",
            "Торговцы",
            "Гилдмастеры",
            "Квестгиверы",
            "Кузнецы",
            "Кожевники",
            "Зельевары",
            "Мастера заклинаний",
        ]

        for category_name in categories_names:
            category, created = AnnouncementCategory.objects.get_or_create(title=category_name)
            self.stdout.write(f"{category.title} created with id: {category.id}")

        self.stdout.write(self.style.SUCCESS(f"All announcements created successfully"))
