from django.contrib.auth import get_user_model
from django.urls import reverse
from owner.models import Owner, Dog
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from unittest.mock import patch

User = get_user_model()

class BaseTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.register_url = reverse('owner:register')
        cls.login_url = reverse('owner:login')
        cls.owner_list_url = reverse('owner:owners-list')
        cls.matches_url = reverse('owner:owner-matches-list')

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
        self.assertEqual(Owner.objects.count(), 3)
        for user_data in self.user_data:
            user = User.objects.get(username=user_data["username"])
            self.assertTrue(Owner.objects.filter(user=user).exists())

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
        owner = Owner.objects.get(user=user)
        self.assertAlmostEqual(float(owner.latitude), 40.7128, places=6)
        self.assertAlmostEqual(float(owner.longitude), -74.0060, places=6)

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

        names = {owner["first_name"] for owner in response.data}
        expected_names = {user["first_name"] for user in self.user_data}

        self.assertSetEqual(names, expected_names)  # Ensure returned users match the registered ones


'''
login
http://localhost:8000/api/login/
input - username, password
outout - token

register
http://localhost:8000/api/register/

{
    "username": "john_doe",
    "password": "securepassword",
    "email": "john_doe@gmail.com",
    "first_name": "John",
    "last_name": "Doe",
    "gender": "male",
    "age": 25,
    "city": "New York",
    "about_me": "Golden retriever lover!",
    "picture": "My picture's url"
}
fa8351cb25d26a897b0910e530651089b7382f66
{
    "username": "jane_smith",
    "password": "anothersecurepassword",
    "email": "jane_smith@gmail.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "gender": "female",
    "age": 30,
    "city": "San Francisco",
    "about_me": "Huskey lover!",
    "picture": "Jane's picture's url"
}
b2a748b79f085b4bff1e476f3535dd159d6a18f1
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
    "picture": "Michael's picture's url"
}

output - User registered successfully!

get_profiles
http://localhost:8000/api/profile/profiles

get_profile/id
http://localhost:8000/api/profile/profiles/{profile_id}

Add using the ModHeader chrome extension: Authorization: Token <your-token-here>
get the token via login page.

set_profile_availability
{
    "owner_username": "john_doe",
    "dog": "Pashosho",
    "place_name": "Dog garden",
    "start_time": "2025-06-23T20:00:00Z",
    "end_time": "2025-06-23T21:00:00Z"
}

Filter by profile and place with Filters in the admin panel (this is changing the url automatically).

NearbyProfilesViewSet
http://localhost:8000/api/owner/nearby-owners/?radius=15

add dog, attach to owner
'''
