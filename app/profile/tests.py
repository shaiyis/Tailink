from django.test import TestCase

# Create your tests here.

'''
login
http://localhost:8000/api/login/
input - username, password
outout - token

register
http://localhost:8000/api/register/

Add hobbies: gaming, soccer, coding, cooking, playing, traveling
{
  "username": "john_doe",
  "password": "securepassword",
  "email": "john_doe@gmail.com",
  "first_name": "John",
  "last_name": "Doe",
  "gender": "male",
  "age": 25,
  "city": "New York",
  "about_me": "I love coding and gaming.",
  "looking_for": "A like-minded individual.",
  "hobbies": [1, 2],
  "picture": "My picture's url"
}
token 58b128d9f87ba2e647fc79587275e53b4f9905f4
{
  "username": "jane_smith",
  "password": "anothersecurepassword",
  "email": "jane_smith@gmail.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "gender": "female",
  "age": 30,
  "city": "San Francisco",
  "about_me": "I'm a tech enthusiast who enjoys hiking.",
  "looking_for": "Someone adventurous and curious.",
  "hobbies": [1, 2],
  "picture": "Jane's picture's url"
}
token 0ba10454fe32a8be28db06b62fb780a971bdd21d
{
  "username": "michael_brown",
  "password": "yetanothersecurepassword",
  "email": "michael_brown@gmail.com",
  "first_name": "Michael",
  "last_name": "Brown",
  "gender": "male",
  "age": 28,
  "city": "Seattle",
  "about_me": "A bookworm who loves exploring coffee shops.",
  "looking_for": "Someone who loves good books and deep conversations.",
  "hobbies": [1, 2],
  "picture": "Michael's picture's url"
}
token 70173159dfb608b66e42d8cd28cbb8c8a22bea21

output - User registered successfully!

get_profiles
http://localhost:8000/api/profiles

get_profile/id
http://localhost:8000/api/profiles/{profile_id}

get_matches
http://localhost:8000/api/matches
Add using the ModHeader chrome extension: Authorization: Token <your-token-here>
get the token via login page.
 
 Tests Done:
 Getting matches when:
   1. age and hobbies matches
   2. more than one hobby in common
   3. more than one profiles matches

 Getting no matches when:
   1. only age matches
   2. only hobbies matches
   3. nothing matches

set_place_and_time
{
    "profile_username": "john_doe",
    "start_time": "2024-12-19T20:00:00Z",
    "end_time": "2024-12-19T21:00:00Z",
    "place_name": "garden"
}

Filter by profile and place with Filters in the admin panel.

NearbyProfilesViewSet
/api/profile/nearby-profiles/{?radius=15}
'''
