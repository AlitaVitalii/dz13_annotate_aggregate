import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from faker import Faker

from myapp.models import Book, Publisher, Author, Store


class Command(BaseCommand):
    help = 'Create books, author, store, publisher'

    def add_arguments(self, parser):
        parser.add_argument('numb', type=int)

    def handle(self, *args, **options):
        fake = Faker()
        a = Author.objects.bulk_create([Author(
            name=fake.name(),
            age=random.randint(30, 70)
        ) for _ in range(options['numb'])])

        b = Book.objects.bulk_create([Book(
            name=fake.language_name(),
            pages=random.randint(100, 500),
            price=random.randint(10, 1000),
            rating=random.randint(1, 10),
            publisher=Publisher.objects.create(name=fake.domain_name()),
            pubdate=fake.date()
        ) for _ in range(options['numb'])])

        for book in b:
            book.authors.add(random.choice(a))

        s = Store.objects.bulk_create([Store(
            name=fake.company()
        ) for _ in range(options['numb'])])

        for store in s:
            store.books.add(random.choice(b))

        self.stdout.write(self.style.SUCCESS(f"Created books: {b}"))
