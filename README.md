# DateNow

DateNow is here to help anyone looking for a relationship to date anywhere and anytime! 👩‍❤️‍👨

Unlike online platforms focusing on virtual interactions, DateNow emphasizes face-to-face connections
to build genuine relationships. DateNow is built using the Python Django REST framework, following a 
Microservices architecture for flexibility and scalability, VScode, Git, and Docker that makes it super
easy to run in every environment with a docker infrastructure.


## Requirements

To use the DateNow, ensure you have the following:

- Docker infrastructure, such as Docker Desktop for Windows or an equivalent for your operating system.
- A modern web browser to access the application.

## Usage

Here’s how to set up and use DateNow:

Build the Docker image:
```bash
docker-compose build
```

Run the application:
```bash
docker-compose up
```

Create a superuser:
```bash
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

Access the admin dashboard: Visit http://localhost:8000/admin in your browser.


## Service Endpoints

Project Service: http://localhost:8000

Profile Service: http://localhost:8001

Place Service: http://localhost:8002


## API Documentation

The API documentation is available at [API Documentation](http://localhost:8000/docs) (Swagger view). 
Below are some example endpoints:



Login: ```POST /api/login``` (implemented with Token Authentication)

Register: ```POST /api/register```

Get Profiles: ```GET /api/profiles```

Get Matches: ```GET /api/matches``` (only logged-in users can see their matches, which are based on age and hobbies in common).

Set Profile Availability: ```POST /api/profile-availability``` (specify place and time)


## Resources for further reading

[Django REST Framework](https://www.django-rest-framework.org/): Understand the framework powering the app.

[drf-spectacular](https://github.com/tfranzel/drf-spectacular/): API schema and documentation tool used.
