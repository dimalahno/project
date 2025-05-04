from django.db import models


class Genre(models.Model):
    """
    Модель для хранения информации о жанрах книг.
    Содержит название жанра и его описание.
    """

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    """
    Модель для хранения информации об авторах книг.
    Содержит основные данные об авторе (имя, биография) и связи с его книгами.
    """

    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Publisher(models.Model):
    """
    Модель для хранения информации об издательствах.
    Содержит название издательства и страну, в которой оно находится.
    """

    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Store(models.Model):
    """
    Модель для хранения информации о магазинах.
    Содержит название магазина и город, в котором он находится.
    """

    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Модель для хранения информации о книгах.
    Содержит основные данные о книге (название, дата публикации, описание)
    и связи с авторами, жанрами, издательствами и магазинами.
    """

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField()
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books', null=True, blank=True)
    stores = models.ManyToManyField(Store, related_name='books')

    def __str__(self):
        return self.title

class Review(models.Model):
    """
    Модель для хранения отзывов о книгах.
    Содержит оценку, комментарий и дату создания отзыва, а также связь с книгой.
    """

    book: Book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Оценка {self.rating} для {self.book.title}"
