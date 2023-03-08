import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

MODEL_FILE = {
    Category: "category.csv",
    Genre: "genre.csv",
    Title: "titles.csv",
    GenreTitle: "genre_title.csv",
    User: "users.csv",
    Review: "review.csv",
    Comment: "comments.csv",
}

KEYS_CHANGE = {
    Comment: ('author', 'author_id'),
    Review: ('author', 'author_id'),
    Title: ('category', 'category_id'),
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for table, file_name in MODEL_FILE.items():
            print('Loading', file_name)
            with open(os.path.join(
                settings.BASE_DIR, 'static', 'data', file_name
            ), encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=',')
                for row in reader:
                    if table in KEYS_CHANGE:
                        key, new_key = KEYS_CHANGE[table]
                        row[new_key] = row.pop(key)
                    table.objects.create(**row)
