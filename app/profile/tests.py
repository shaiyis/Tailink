from django.contrib.auth import get_user_model
from django.urls import reverse
from profile.models import Profile, Hobby
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from unittest.mock import patch

User = get_user_model()

class BaseTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.register_url = reverse('profile:register')
        cls.login_url = reverse('profile:login')
        cls.profile_list_url = reverse('profile:profiles-list')
        cls.matches_url = reverse('profile:profile-matches-list')

        # Insert predefined hobbies
        hobbies = ["gaming", "soccer", "coding", "cooking", "playing", "traveling"]
        for hobby in hobbies:
            Hobby.objects.get_or_create(name=hobby)

        cls.user_data = [
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
        # Register profiles
        for user_data in cls.user_data:
            response = cls.client.post(cls.register_url, user_data, format='json')
            assert response.status_code == 201, f"Registration failed for {user_data['username']}"
            assert response.data['message'] == 'User registered successfully!', f"Unexpected response message: {response.data}"


class UserRegisterApiViewTest(BaseTestCase):
    def test_registered_users_exist(self):
        """Test that the registered users exist in the database."""
        self.assertEqual(Profile.objects.count(), 3)
        for user_data in self.user_data:
            user = User.objects.get(username=user_data["username"])
            self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_invalid_registration(self):
        """Test registration fails with missing fields."""
        response = self.client.post(self.register_url, {"username": "incomplete_user"}, format='json')
        self.assertEqual(response.status_code, 400)
        # ensure that the API correctly returns validation errors when required fields are missing
        self.assertIn('password', response.data)
        self.assertIn('email', response.data)


class UserLoginApiViewTest(BaseTestCase):
    @patch('profile.views.get_current_location')  # Mock location service
    def test_valid_token_is_accepted(self, mock_location):
        """Test that a valid token is returned and associated with the correct user."""
        mock_location.return_value = {'latitude': 40.7128, 'longitude': -74.0060}  # Mock location data
        profile_data = self.user_data[0]
        response = self.client.post(self.login_url, {'username': profile_data['username'], 'password': profile_data['password']})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        
        token = response.data['token']
        user = User.objects.get(username=profile_data['username'])
        self.assertTrue(Token.objects.filter(key=token).exists())
        self.assertEqual(Token.objects.get(key=token).user, user)

        # Check if location was updated
        profile = Profile.objects.get(user=user)
        self.assertAlmostEqual(float(profile.latitude), 40.7128, places=6)
        self.assertAlmostEqual(float(profile.longitude), -74.0060, places=6)

    def test_invalid_credentials(self):
        """Test login fails with invalid credentials."""
        profile_data = self.user_data[0]
        response = self.client.post(self.login_url, {'username': profile_data['username'], 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 400)
        self.assertNotIn('token', response.data)
                  

class ProfileViewSetTest(BaseTestCase):
    def test_get_profiles(self):
        """Test that all registered profiles are returned."""
        response = self.client.get(self.profile_list_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)  # Ensure all three profiles are returned

        names = {profile["first_name"] for profile in response.data}
        expected_names = {user["first_name"] for user in self.user_data}

        self.assertSetEqual(names, expected_names)  # Ensure returned users match the registered ones


class ProfileMatchesViewSetTest(BaseTestCase):
    def test_profile_matches(self):
        """Test that jane_smith is a match for john_doe."""
        # Authenticate as john_doe
        login_response = self.client.post(reverse('profile:login'), {
            'username': 'john_doe',
            'password': 'securepassword'
        }, format='json')
        self.assertEqual(login_response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {login_response.data['token']}")

        response = self.client.get(self.matches_url)
        self.assertEqual(response.status_code, 200)
        
        expected_matches = {"Jane"}
        returned_matches = {profile["first_name"] for profile in response.data}
        
        self.assertSetEqual(expected_matches, returned_matches)


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
http://localhost:8000/api/profile/profiles

get_profile/id
http://localhost:8000/api/profile/profiles/{profile_id}

get_matches
http://localhost:8000/api/profile/matches
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

set_profile_availability
{
    "profile_username": "john_doe",
    "start_time": "2024-12-19T20:00:00Z",
    "end_time": "2024-12-19T21:00:00Z",
    "place_name": "garden"
}

Filter by profile and place with Filters in the admin panel.

NearbyProfilesViewSet
http://localhost:8000/api/profile/nearby-profiles/?radius=15
'''
