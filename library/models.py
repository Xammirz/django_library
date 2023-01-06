from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """

    name = models.CharField(
        max_length=200, help_text="Введите жанр книги", verbose_name="Имя"
    )

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """

    title = models.CharField(max_length=200, verbose_name="Имя")
    author = models.ForeignKey(
        "Author",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Автор",
        related_name="+",
    )

    summary = models.TextField(
        max_length=1000,
        help_text="Напишите описание этой книге",
        verbose_name="Описание",
    )
    isbn = models.CharField(
        "ISBN",
        max_length=13,
    )
    genre = models.ManyToManyField(
        Genre, help_text="Выберите жанр для этой книги", verbose_name="Жанр"
    )

    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the book",
        verbose_name="Описание",
    )
    isbn = models.CharField(
        "ISBN",
        max_length=13,
    )
    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book", verbose_name="Жанр"
    )

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):

        return ", ".join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = "Genre"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class BookInstance(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular book across whole library",
    )

    book = models.ForeignKey(
        "Book", on_delete=models.SET_NULL, null=True, verbose_name="Книга"
    )
    imprint = models.CharField(max_length=200, verbose_name="Издательство")
    due_back = models.DateField(null=True,
                                blank=True,
                                verbose_name="Срок годности до:")
    borrower = models.ForeignKey(User,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ("m", "Обслуживающий"),
        ("o", "В кредит"),
        ("a", "В наличии"),
        ("r", "Забронирован"),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Наличие книги",
        verbose_name="Статус",
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability",
        verbose_name="Статус",
    )

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)
        verbose_name = "Копия книги"
        verbose_name_plural = "Копии книг"

    def __str__(self):
        """
        String for representing the Model object
        """
        return "%s (%s)" % (self.id, self.book.title)


class Author(models.Model):
    """
    Model representing an author.
    """

    book = models.ForeignKey(
        "Book",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Книга",
        related_name="+",
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name="Дата рождения"
    )
    date_of_death = models.DateField("Дата смерти", null=True, blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return "%s, %s" % (self.last_name, self.first_name)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["last_name"]
