from rest_framework import serializers

from library.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "summary", "isbn"]
