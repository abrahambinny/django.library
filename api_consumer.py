""" Api Consumer module
    
    Description: This module is used to call and test the apis created in this project
"""

import requests
from requests.auth import HTTPBasicAuth

LOGIN_CREDENTIALS = {
    'staff': {
        'username': 'staffuser',
        'password': 'test@123'
    },
    'webuser': {
        'username': 'binny',
        'password': 'test@123'
    },
}

def get_search_api():

    response = requests.get(
        "http://127.0.0.1:8000/api/books/search/?book-search=george&format=json",
        auth=HTTPBasicAuth(
            LOGIN_CREDENTIALS['webuser']['username'], 
            LOGIN_CREDENTIALS['webuser']['password']
        )
    )
    return response.text


def get_wishlist_api():
    
    response = requests.get(
        "http://127.0.0.1:8000/api/wishlist/7/?format=json",
        auth=HTTPBasicAuth(
            LOGIN_CREDENTIALS['webuser']['username'], 
            LOGIN_CREDENTIALS['webuser']['password']
        )
    )
    return response.text


def create_wishlist_api():
    
    post_data = {
        "id": 1,
        "book": 93,
        "user": 2
    }
    
    response = requests.put(
        "http://127.0.0.1:8000/api/wishlist/7/?format=json",
        data = post_data,
        auth=HTTPBasicAuth(
            LOGIN_CREDENTIALS['webuser']['username'], 
            LOGIN_CREDENTIALS['webuser']['password']
        )
    )
    return response.text

def modify_availability():
    
    post_data = {
        "title": "Twilight",
        "author": "Stephenie Meyer",
        "available": 'true'
    }
    
    response = requests.put(
        "http://127.0.0.1:8000/api/available/93/?format=json",
        data = post_data,
        auth=HTTPBasicAuth(
            LOGIN_CREDENTIALS['staff']['username'], 
            LOGIN_CREDENTIALS['staff']['password']
        )
    )
    return response.text

def generate_report():
    
    response = requests.get(
        "http://127.0.0.1:8000/api/report/generate/?format=json",
        auth=HTTPBasicAuth(
            LOGIN_CREDENTIALS['staff']['username'], 
            LOGIN_CREDENTIALS['staff']['password']
        )
    )
    return response.text
    
    


if __name__ == "__main__":
    
    print(get_search_api())
    print(get_wishlist_api())
    print(create_wishlist_api())
    print(modify_availability())
    print(generate_report())
    