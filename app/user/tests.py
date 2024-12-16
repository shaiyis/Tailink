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
{
  "username": "jane_smith",
  "password": "anothersecurepassword",
  "email": "jane_smith@gmail.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "age": 30,
  "city": "San Francisco",
  "about_me": "I'm a tech enthusiast who enjoys hiking.",
  "looking_for": "Someone adventurous and curious.",
  "hobbies": [3, 4],
  "picture": "Jane's picture's url"
}
{
  "username": "michael_brown",
  "password": "yetanothersecurepassword",
  "email": "michael_brown@gmail.com",
  "first_name": "Michael",
  "last_name": "Brown",
  "age": 28,
  "city": "Seattle",
  "about_me": "A bookworm who loves exploring coffee shops.",
  "looking_for": "Someone who loves good books and deep conversations.",
  "hobbies": [5, 6],
  "picture": "Michael's picture's url"
}
'''
#output - User registered successfully

#get_profiles
#http://localhost:8000/admin/user/profiles

#get_profile/id
#http://localhost:8000/admin/user/profile/{profile_id}