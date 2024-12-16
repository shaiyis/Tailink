from django.test import TestCase

# Create your tests here.

# login
# http://localhost:8000/api/login/
# input - username, password
# outout - token

# register
# http://localhost:8000/api/register/
'''
{
  "username": "john_doe",
  "password": "securepassword",
  "email": "john_doe@gmail.com",
  "first_name": "John",
  "last_name": "Doe",
  "age": 25,
  "city": "New York",
  "about_me": "I love coding and gaming.",
  "looking_for": "A like-minded individual.",
  "hobbies": [1, 2],
  "picture": "My picture's url"
}
'''
#output - User registered successfully