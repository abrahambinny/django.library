# books/inventory/serializers.py
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ["id", "title", "author", "language", "book_id", "isbn", "available", "pub_year"]