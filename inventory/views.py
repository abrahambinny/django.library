from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User

# Create your views here.


# book/inventory/views.py
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import permissions, viewsets
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import filters

from .models import Book, Wishlist
from .serializers import BookSerializer, WishlistSerializer, UserSerializer
from inventory.permissions import IsStaffUserAuthenticated


class BookViewSet(viewsets.ModelViewSet):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    
    @action(detail=False, methods=["get"])
    def search(self, request):
        books_filter = self.get_queryset().filter(Q(title__icontains=self.request.query_params.get('book-search', '')) | Q(author__icontains=self.request.query_params.get('book-search', '')))
        serializer = self.get_serializer(books_filter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # @action(detail=False, methods=["get"])
    # def title(self, request):
    #     books = self.get_queryset().filter(title__icontains=self.request.query_params.get('book-title', ''))
    #     serializer = self.get_serializer(books, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    # @action(detail=False, methods=["get"])
    # def author(self, request):
    #     books = self.get_queryset().filter(author__icontains=self.request.query_params.get('book-author', ''))
    #     serializer = self.get_serializer(books, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=["get"])
    # def available(self, request):
    #     books = self.get_queryset().filter(available=self.request.query_params.get('book-available', ''))
    #     serializer = self.get_serializer(books, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class WishlistViewSet(viewsets.ModelViewSet):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    queryset = Wishlist.objects.all().order_by('created_time')
    serializer_class = WishlistSerializer
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def perform_delete(self, serializer):
        serializer.save(user=self.request.user)

    
class UserViewSet(viewsets.ModelViewSet):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
