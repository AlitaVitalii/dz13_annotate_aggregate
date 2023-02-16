import random

from django.core.management import BaseCommand
from faker import Faker

from myapp.models import Publisher, Author, Book, Store


class Command(BaseCommand):
    help = 'Create 100-books, 100-author, 10-store, 10-publisher'

    def handle(self, *args, **options):
        fake = Faker()
        Publisher.objects.all().delete()
        Book.objects.all().delete()
        Store.objects.all().delete()
        Author.objects.all().delete()

        # create 10-publishers
        publishers = Publisher.objects.bulk_create([Publisher(name=fake.domain_name()) for _ in range(10)])

        # create 100-books
        for publisher in publishers:
            Book.objects.bulk_create([Book(
                name=fake.street_name(),
                pages=random.randint(100, 500),
                price=random.randint(10, 1000),
                rating=random.randint(1, 10),
                publisher=publisher,
                pubdate=fake.date()
            ) for _ in range(10)])

        # create 100-authors
        authors = Author.objects.bulk_create([Author(
            name=fake.name(),
            age=random.randint(30, 70)
        ) for _ in range(100)])

        # create 10-stores
        stores = Store.objects.bulk_create([Store(
            name=fake.company()
        ) for _ in range(10)])

        books = list(Book.objects.all())
        for store in stores:
            temp = []
            for i in range(10):
                temp.append(books.pop(0))
            store.books.set(temp)
            store.save()

        b = Book.objects.all()
        for book in b:
            book.authors.add(random.choice(authors))

        for i, book in enumerate(b):
            book.authors.add(authors[i])

        self.stdout.write(self.style.SUCCESS(f"Created books: {b}"))
