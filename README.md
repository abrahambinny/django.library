
# Create Backend of a web App to handle book loans on a small library

## Implemented the following tasks within the project

- Create Backend for a Web App using Python, Django & Django Rest Framewwork

- Included admin panel to check the data

- Features implemented on the Backend API's

    - For Library Website Users:
        - An endpoint that allows the database searching by title and by author, returning books and their availability.

        - Add/remove unavailable books to/from a wishlist such that they are notified when they become available for Library

    - For Library Staff:
        - Change the rental status (available/borrowed) for a book (which should also trigger the email notifications to users with the book in their wishlist)

        - Generate a report on the number of books being rented and how many days they’ve been rented for.

        - The frontend of the library website displays affiliate links to copies of the book available on Amazon for each book. (Didnt find the exact apis for the same)


### Componets used

- Python==3.8.10
- Django==4.0.6
- djangorestframework==3.13.1
- django-filter==22.1
- SQLite DB


### Steps to create the Backend Api

- Create Virtual Environment

    `python -m venv .venv`

- Activate Virtual Environment

    `source .venv/bin/activate`

- Install the modules required

    `pip install -r requirements.txt`

- Create the django project

    `django-admin startproject book`

    `cd book`

- Create the django app

    `python manage.py startapp inventory`

- Sync your database for the first time:

    `python manage.py makemigrations`

    `python manage.py migrate`

- Create a super user for the admin tool

    `python manage.py createsuperuser --email abrahambinny@gmail.com --username admin`

- Installing a django app

    modify the INSTALLED_APPS variable by adding the inventory app & rest_framework 

    Application definition

        INSTALLED_APPS = ['django.contrib.admin',

        'django.contrib.auth',

        'django.contrib.contenttypes',

        'django.contrib.sessions',

        'django.contrib.messages',

        'django.contrib.staticfiles',

        # Custom apps

        'rest_framework',

        'inventory',

        'django_filters',
        
        ]

- Create the Book model

    Creates a model `class Book(models.Model):` with the following fields. This model is basically used to store the given Backend Data which consits of the Books and details. Following fields I created to store the details.

        id -> Primary key of each book

        title  -> Title of the book

        author -> Authors of the book

        language -> language in which book written

        book_id -> Amazon book Id

        isbn -> isbn numbers of each books

        available -> avialibility flag in which the book is available for rent or loan or not.

        pub_year -> Publication year of the book

        created_time -> Entry created time

        updated_time -> Modification time when each the status of availability changes.

- Create the Wishlist model

    Wishlist model `class Wishlist(models.Model):` is created to store the wishlish of each users. Whenever any users add/remove the books to this wishlist it willl be moved to this wishlist model. Wishlist can be search obased on each book and the users. The users have visbility only to their on wishlist other than admin/staff user.

        book -> Foreign key to Book Model. Each Book stored here is relationship with Book Model

        user -> Foreign key to django auth User Model. Each entry here is related to a particular user on User model

        created_time -> Entry created time

        updated_time -> Modification time when each the status of availability changes. And it stored the latest availabilty/borrow start time.

- Sync your database for the models created:

    `python manage.py makemigrations`

    `python manage.py migrate`


- Create Serializers

    create a new module named `inventory/serializers.py` and created the below serializers inside. Serilaise we are used for the data representation for API.

    1. `class BookSerializer(serializers.ModelSerializer):` 
        
        This serializer is used to serialize the Book model for API responses
            
    2. `class WishlistSerializer(serializers.ModelSerializer):`
        
        This serializer is used to serialize the Wishlist model for API responses
            
    3. `class UserSerializer(serializers.ModelSerializer):`
        
        This serializer is used to serialize the User model for API responses
            
    4. `class AvailableSerializer(serializers.ModelSerializer):`
        
        This serializer is used to made upon the Book model to create the availability endpoint. I made it separate to separate it from the normal Book API activaties. This is written specifically for the change in availability status and mail triggering responses.
            
    5. `class ReportSerializer(serializers.ModelSerializer):`
        
        This serializer is used to made upon the Wishlist model to create the generator report endpoint. I made it separate to separate it from the normal Wishlist API activaties. This is written specifically for generate report API endpoint.

- Creating views

    I wrote separate views for each Endpoints:

    ### For Library Website Users:

    1. `class BookViewSet(viewsets.ModelViewSet):`

        BookViewSet is used to do the search functionality on the Books in the database based on title and author

        `@action(detail=False, methods=["get"])`
        `def search(self, request):`

        This search GET method is used to implement the search endpoint

        `http://127.0.0.1:8000/api/books/search/?book-search=george&format=json`

            Response

                [
                    {
                    "id": 128,
                    "title": "A Game of Thrones",
                    "author": "George R.R. Martin",
                    "available": false
                    },
                    {
                    "id": 104,
                    "title": "Animal Farm: A Fairy Story",
                    "author": "George Orwell",
                    "available": true
                    },
                    {
                    "id": 103,
                    "title": "Nineteen Eighty-Four",
                    "author": "George Orwell, Erich Fromm, Celâl Üster",
                    "available": true
                    }
                ]
        
    2. `class WishlistViewSet(viewsets.ModelViewSet):`

        WishlistViewSet is used to do Add/remove unavailable books to/from a wishlist such that they are notified when they become available. I restricted the view in such a way that each user can see their only wishlist. Only the library staff and admin can view and perform every users wish actions.

        GET

        To get the list of users in wishlist

        `http://127.0.0.1:8000/api/wishlist/?format=json`

            Response

                [
                    {
                    "id": 1,
                    "book": 93,
                    "user": 2
                    },
                    {
                    "id": 2,
                    "book": 99,
                    "user": 5
                    },
                    {
                    "id": 3,
                    "book": 97,
                    "user": 4
                    },
                    {
                    "id": 4,
                    "book": 109,
                    "user": 2
                    }
                ]

        POST

        To Add/update the user in to the wishlist

        `http://127.0.0.1:8000/api/wishlist/7/?format=json`

            Response

                {
                    "id": 7,
                    "book": 155,
                    "user": 2
                }
                        
    ### For Library Staff:

    3. `class UpdateAvailability(viewsets.ModelViewSet):`

        Change the rental status (available/borrowed) for a book (which should also trigger the email notifications to users with the book in their wishlist)

        `def update(self, request, *args, **kwargs):`

        I have overrided the perform_update function to include our logic of triggering mail on the change in status from available to borrowed and viceversa.


        POST

        `http://127.0.0.1:8000/api/available/93/?format=json`

            This will modify the availability of a particular book. And send mail to the users who add this particular book in their wishlist

            Request 
                {
                    "title": "Twilight",
                    "author": "Stephenie Meyer",
                    "available": true
                }

            Response

                {
                    "status": "success",
                    "message": "Availabilty updated successfully and Sent mail to the users",
                    "email_content": [
                        {
                            "email_content": "The book Twilight in your wishlist changed status to Available",
                            "username": "Binny",
                            "email": "abrahambinny@gmail.com"
                        }
                    ]
                }

    4. `class GenerateReportViewSet(viewsets.ModelViewSet):`

        Generate a report on the number of books being rented and how many days they have been rented for.

        `@action(detail=False, methods=["get"])`
        `def generate(self, request):`

        This generate GET method is used to implement the generate report function. This will generate report on the rented books and their rented date

        GET

        `http://127.0.0.1:8000/api/report/generate/?format=json`

        Response

                {
                    "rented_books": [
                        {
                            "book": "The Fellowship of the Ring",
                            "rented_date": "2022-08-01"
                        },
                        {
                            "book": "A Game of Thrones",
                            "rented_date": "2022-08-01"
                        }
                    ]
                }

        
    - Registering urls in `inventory/urls.py`

            router.register(r'books', views.BookViewSet)
            router.register(r'wishlist', views.WishlistViewSet)
            router.register(r'users', views.UserViewSet)
            router.register(r'available', views.UpdateAvailability)
            router.register(r'report', views.GenerateReportViewSet)

    - Include the api url path in project urls `book/urls.py`
            
            urlpatterns = [
                path('admin/', admin.site.urls),
                path('api-auth/', include('rest_framework.urls')),
                path('api/', include('inventory.urls')),
            ]
            
    - Create `inventory/permissions.py` to override the django rest framework permissions based on our API permissions

        `class IsOwnerOrReadOnly(permissions.BasePermission):`

        `class IsStaffUserAuthenticated(permissions.BasePermission):`

    - Included the models in to `inventory/admin.py` inorder to do admin level activities. Add records, add users etc.

        `admin.site.register(Book)`
        `admin.site.register(Wishlist)`


- To populate the data into db `sqlite_connection.py`

        python sqlite_connection.py


- To run the django server

        python manage.py runserver


- Written an api consumer file `api_consumer.py` to consume the apis created

        python api_consumer.py