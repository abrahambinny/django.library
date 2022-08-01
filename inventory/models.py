from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=250, db_index=True, blank=True, null=True)
    author = models.CharField(max_length=250, db_index=True, blank=True, null=True)
    language = models.CharField(max_length=10, db_index=True, default="eng")
    book_id = models.IntegerField()
    isbn = models.CharField(max_length=50)
    available = models.BooleanField(default=True, blank=True)
    pub_year = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.title
    

    

