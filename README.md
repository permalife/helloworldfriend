# HelloWorldFriend

## What it is
A web service for time-delayed messaging of people

## How it works
There are three main components to the project:

1. Django app that runs on `gunicorn` (WSGI HTTP Server)
2. Celery task queue that processes greeting requests
3. RabbitMQ messaging server that serves as a broker between 1. and 2.

## Installation

To download the package and install its dependencies, run:

```
sudo pip install -e git+git@github.com:permalife/helloworldfriend#egg=helloworldfriend
```

This will place the source code to `./src/helloworldfriend` and install all project dependencies, except `rabbitmq-server`. The latter needs to be installed using one of the methods described [here](https://www.rabbitmq.com/download.html).

## Getting it up and running

The app lives in its root folder:
```
cd helloworld
```

It is managed by `supervisord` process manager. To start supervisord:
```
sudo supervisord -c supervisord.conf
```

To check that all three services are running:
```
sudo supervisorctl status
```
which on my sandbox results in:
```
celeryhwf                        RUNNING   pid 77340, uptime 3:18:36
gunicorn                         RUNNING   pid 81496, uptime 2:14:03
rabbitmq-server                  RUNNING   pid 77339, uptime 3:18:36
```
For each of the services the output is directed to a log file, `<service_name>.log`. If supervisor fails to locate a particular service, the corresponding log file will have the necessary information. Note that it expects each of three services to be found in the system `PATH`.

The web server is started on port `8000` and the endpoint served by the app is at `http://localhost:8000/greet/`

## Testing the app
To quickly test several common use cases, run:
```
python manage.py test
```

This uses Django testing framework to run five unit tests, all of which should pass. The unit tests are located in `hwf/tests.py` for reference.

Another way to test the service is using `curl` tool, e.g.:
```
curl -i -X POST -H 'Content-Type: application/json' -d '{"name": "Joe", "datetime": "20151113080900"}' http://localhost:8000/greet/
```

The greeting time is represented by a string of the form `YYYYMMDDHHMMSS`, which is specified in UTC. The example above should fail with a status code *400* because the requested greeting time is in the past.

Once a valid datetime string is posted along with a friend's name, the app will spin off a time-delayed celery background task that will log the greeting to `celeryhwf.log` at the specified time.

## What else is in the bag
The rest of code is structured as follows:
```
helloworld/
    helloworld/		# django settings and url resolvers
    hwf/
        celeryhwf/      # celery configuration and tasks
        migrations/
        templates/      # basic template for rendering response to the user
        __init_.py
        admin.py
        forms.py        # django form instance to handle the request data
        models.py
        tests.py        # unittests spanning several test cases
        views.py        # url handler using django's view subclass  
```

## More information
I realize that the installation of the app is not 100% automated. Should you encounter any problems with getting the app up and running, please shoot me an email. Most likely, it is a really quick thing.
