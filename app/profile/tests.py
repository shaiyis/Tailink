from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from unittest.mock import patch
from profile.models import Profile, Hobby

User = get_user_model()

class UserRegisterApiViewTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('profile:register')

        # Insert predefined hobbies
        hobbies = ["gaming", "soccer", "coding", "cooking", "playing", "traveling"]
        for hobby in hobbies:
            Hobby.objects.get_or_create(name=hobby)

        self.user_data = [
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
                "hobbies": ["gaming", "soccer"],
                "picture": "My picture's url"
            },
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
                "hobbies": ["gaming", "soccer"],
                "picture": "Jane's picture's url"
            },
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
                "hobbies": ["gaming", "soccer"],
                "picture": "Michael's picture's url"
            }
        ]
    
    def test_user_registration(self):
        """Test that a user can successfully register."""
        for user_data in self.user_data:
            if not User.objects.filter(username=user_data["username"]).exists():
              response = self.client.post(self.register_url, user_data, format='json')
              self.assertEqual(response.status_code, 201)
              self.assertEqual(response.data['message'], 'User registered successfully!')
              self.assertTrue(User.objects.filter(username=user_data['username']).exists())

    def test_invalid_registration(self):
        """Test registration fails with missing fields."""
        response = self.client.post(self.register_url, {"username": "incomplete_user"}, format='json')
        self.assertEqual(response.status_code, 400)
        # ensure that the API correctly returns validation errors when required fields are missing
        self.assertIn('password', response.data)
        self.assertIn('email', response.data)


class UserLoginApiViewTest(UserRegisterApiViewTest):
    def setUp(self):
        super().setUp()
        self.login_url = reverse('profile:login')
        self.test_user = self.user_data[0]
        self.client.post(self.register_url, self.test_user, format='json')

    @patch('profile.views.get_current_location')  # Mock location service
    def test_valid_token_is_accepted(self, mock_location):
        """Test that a valid token is returned and associated with the correct user."""
        mock_location.return_value = {'latitude': 40.7128, 'longitude': -74.0060}  # Mock location data

        response = self.client.post(self.login_url, {'username': self.test_user['username'], 'password': self.test_user['password']})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        
        token = response.data['token']
        user = User.objects.get(username=self.test_user['username'])
        self.assertTrue(Token.objects.filter(key=token).exists())
        self.assertEqual(Token.objects.get(key=token).user, user)

        # Check if location was updated
        profile = Profile.objects.get(user=user)
        self.assertAlmostEqual(float(profile.latitude), 40.7128, places=6)
        self.assertAlmostEqual(float(profile.longitude), -74.0060, places=6)

    def test_invalid_credentials(self):
        """Test login fails with invalid credentials."""
        response = self.client.post(self.login_url, {'username': self.test_user['username'], 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 400)
        self.assertNotIn('token', response.data)

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
  "hobbies": ["gaming", "soccer"],
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
  "hobbies": ["gaming", "soccer"],
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
  "hobbies": ["gaming", "soccer"],
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
