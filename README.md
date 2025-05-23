# Задание Lite
1. Как изменился бы запрос, если бы мы использовали ForeignKey вместо ManyToManyField?
- Если бы связь Book и Genre была через ForeignKey, это означало бы, что каждая книга могла принадлежать только одному жанру, а не нескольким.
- поиск книг, принадлежащих двум жанрам одновременно, уже невозможен
2. Какие проблемы могут возникнуть при использовании ManyToManyField?
- Производительность запросов: в ManyToManyField связь реализуется через промежуточную таблицу (book_genres), поэтому Django выполняет JOIN-запросы к ней. Это может замедлить работу, если база данных очень большая.
- Сложность фильтрации: например, если нужно найти книги, принадлежащие одновременно двум жанрам ("Фантастика" и "Детектив"), запрос становится сложнее:
- Трудности с удалением: если удалить жанр (Genre), нужно убедиться, что связи в ManyToManyField тоже корректно обновлены. Например, при on_delete=models.CASCADE все книги, связанные с этим жанром, не удалятся, но потеряют связь с ним.


# Задания Pro
Доступ к админ-панели
- login: admin
- password: 123

### 1. Полное описание созданных моделей, включая объяснение связей между ними.
- Добавлены комментарии к классам 
----
### 2. Пошаговые инструкции по созданию тестовых данных для издательств, магазинов и книг через административную панель.
- Данные созданы через административную панель и через shell. 
- Сначала созданы данные об авторах, магазинах, жанрах, издателях.
- Затем добавлены книги с установкой связей.
- К каждой книге добавлены обзоры
----
### 3. Описание выполненных запросов, объясняя их логику и результаты.
1. **Напишите запрос для нахождения всех книг, опубликованных издательствами из определённой страны.**
from books.models import Book, Publisher
country_name = "Россия"
books = Book.objects.filter(publisher__country=country_name)
- Мы ищем все издательства (Publisher), у которых country соответствует заданному значению.
- Используем связь ForeignKey(publisher), чтобы найти все Book, которые связаны с издательствами из выбранной страны.
----
2. **Получите список всех книг, которые продаются в магазине в определённом городе.**
- city_name = "Москва"
- stores_in_city = Store.objects.filter(city=city_name)
- books_in_stores = Book.objects.filter(stores__in=stores_in_city).distinct()
- Фильтруем Store, выбирая магазины, у которых city="Москва".
- Используем Book.objects.filter(stores__in=stores_in_city), чтобы выбрать книги, которые связаны с найденными магазинами.
- Добавляем .distinct(), чтобы исключить дубликаты, если одна и та же книга продается в нескольких магазинах города.
----
3. **Найдите все книги, которые имеют среднюю оценку выше определённого значения**
- min_rating = 4.5 
- books = Book.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gt=min_rating)
----
4. **Подсчитайте количество книг, продающихся в каждом магазине.**
- stores = Store.objects.annotate(book_count=Count("books"))
- for store in stores: print(f"Магазин: {store.name}, Количество книг: {store.book_count}")
----
5. **Найдите магазины, где продаются книги, опубликованные после определённой даты**
- publication_date_threshold = "2010-01-01"
- stores = Store.objects.filter(books__published_date__gt=publication_date_threshold).annotate(book_count=Count("books")).order_by("-book_count")
- for store in stores: print(f"Магазин: {store.name}, Город: {store.city}, Количество продаваемых книг: {store.book_count}")
----

### 4. Пояснения к тому, как была выполнена оптимизация запросов с использованием select_related() и prefetch_related().

----
1. Оптимизация запроса: Книги и их издатели (select_related())
Когда связь между Book и Publisher — ForeignKey, можно использовать select_related(), чтобы сократить количество SQL-запросов.
from books.models import Book

books = Book.objects.select_related("publisher").all()

for book in books:
    print(f"Книга: {book.title}, Издательство: {book.publisher.name}")

Логика запроса:
- select_related("publisher") делает один SQL-запрос, сразу загружая Publisher.
- Это ускоряет выполнение, так как Django не делает отдельные запросы для каждого Book.publisher.

2. Оптимизация запроса: Книги, магазины и отзывы (prefetch_related())
Если связь "многие ко многим" (ManyToManyField), лучше использовать prefetch_related(), которое загружает связанные данные в отдельных запросах, но оптимизирует их для массовой загрузки.
from books.models import Book

books = Book.objects.prefetch_related("stores", "reviews").all()

for book in books:
    print(f"Книга: {book.title}")
    print(f"Продается в магазинах: {[store.name for store in book.stores.all()]}")
    print(f"Отзывы: {[review.comment for review in book.reviews.all()]}")

Логика запроса:
- prefetch_related("stores", "reviews") загружает все связанные магазины и отзывы одним запросом, вместо отдельных вызовов для каждой книги.
- Django делает один SQL-запрос для Book и отдельные запросы для Store и Review, но кэширует их для оптимального доступа.




