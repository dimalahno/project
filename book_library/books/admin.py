from django.contrib import admin
from .models import Author, Book, Genre, Publisher, Review, Store

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Publisher)
admin.site.register(Review)
admin.site.register(Store)
