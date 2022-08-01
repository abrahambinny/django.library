from django.shortcuts import render

# Create your views here.


# book/inventory/views.py
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import permissions, viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer


    @action(detail=False, methods=["get"])
    def available(self, request):
        books = self.get_queryset().filter(available=True)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"])
    def search(self, request):
        books_filter = self.get_queryset().filter(title__icontains=self.request.query_params.get('book-search', ''))
        serializer = self.get_serializer(books_filter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)