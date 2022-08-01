# books/inventory/serializers.py
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Book, Wishlist

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ["id", "title", "author", "available"]
        
class WishlistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Wishlist
        fields = ["id", "book"]
        
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]