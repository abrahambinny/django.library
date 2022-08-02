
# book/inventory/views.py

from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime

from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework import status
from rest_framework import permissions, viewsets
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import filters

from .models import Book, Wishlist
from .serializers import BookSerializer, WishlistSerializer, UserSerializer, AvailableSerializer, ReportSerializer
from inventory.permissions import IsStaffUserAuthenticated


    
class BookViewSet(viewsets.ModelViewSet):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    # lookup_field = 'available'
    
    @action(detail=False, methods=["get"])
    def search(self, request):
        books_filter = self.get_queryset().filter(Q(title__icontains=self.request.query_params.get('book-search', '')) | Q(author__icontains=self.request.query_params.get('book-search', '')))
        serializer = self.get_serializer(books_filter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class WishlistViewSet(viewsets.ModelViewSet):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    queryset = Wishlist.objects.all().order_by('created_time')
    serializer_class = WishlistSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        else:
            return self.queryset.filter(user=self.request.user)         
    
    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(user=self.request.user)
        
    def perform_delete(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(user=self.request.user)

    
class UserViewSet(viewsets.ModelViewSet):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class UpdateAvailability(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = AvailableSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.available = request.data.get("available", False)
        if instance.available == 'true':
            instance.available = True
        else:
            instance.available = False
        instance.save()
        
        wishObj = Wishlist.objects.filter(book=instance)
        if wishObj:
            email_lst = []
            status_map = {True: 'Available', False: 'Borrowed'}
            email_subject = f"The book {instance.title} in your wishlist changed status to {status_map[instance.available]}"
            for item in wishObj:
                email_dct = {}
                email_dct['email_content'] = email_subject
                user = item.user
                email_dct['username'] = user.first_name
                email_dct['email'] = user.email
                email_lst.append(email_dct)

            response_dct = {
                "status": "success",
                "message": "Availabilty updated successfully and Sent mail to the users",
                "email_content": email_lst
            }
        else:
            response_dct = {
                "status": "fail",
                "message": f"The book {instance.title} is not in any of the users wishlist",
            }
            
        return Response(response_dct, status=status.HTTP_200_OK)
    
    
class GenerateReportViewSet(viewsets.ModelViewSet):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAdminUser]
    queryset = Wishlist.objects.all().order_by('created_time')
    serializer_class = ReportSerializer
    
    @action(detail=False, methods=["get"])
    def generate(self, request):
        rented_lst = []
        for item in self.get_queryset():
            if not item.book.available:
                rented_lst.append({"book": item.book.title, "rented_date": datetime.strftime(item.updated_time, "%Y-%m-%d")})
                
        return Response({"rented_books": rented_lst}, status=status.HTTP_200_OK)
    
    
