# Friend's Gallery

## Setting Environment

To get the project running, just execute:
- `docker-compose up -d`

## First Run

When you run the project for the first time, you'll need to run the following commands:
- `docker exec -it friends-gallery-server_web_1 bash`
- `python manage.py migrate --settings=settings.local`

## Create Admin User

Inside the container, run:
- `python manage.py createsuperuser --settings=settings.local`


After following the steps above, everything should be working now :) enjoy

----

This project has a client that consumes this API
## Client

- Repository: https://github.com/victorescoto/friends-gallery-client
