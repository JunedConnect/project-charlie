## Project structure
The project is called `digital_journal`.  It currently consists of a single app `journals`.

## Deployed version of the application
The deployed version of the application can be found at [*enter url here*](*enter_url_here*).

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py makemigrations

$ python3 manage.py migrate
```

Initialise Universal Journal Templates

```
$ python3 manage.py startserver
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

<<<<<<< HEAD
Create code coverage report with:
```
$ coverage run manage.py test
```

See code coverage report with:
```
$ coverage report
```

Create html file with code coverage report:
```
$ coverage html
=======
Install Homebrew (THE FOLLOWING IS SERVER INSTRUCTIONS FOR MACOS)

```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Update and install redis

```
$ brew update
$ brew install redis
```

Install Python Certificates (macOS)

```
$ /Applications/Python\ 3.11/Install\ Certificates.command
```

Update environment variables for SSL certification

```
$ export SSL_CERT_FILE=$(python -m certifi)
```

Run redis on a new (second) terminal

```
$ redis-server   
```

Run celery worker on a new (third) terminal

```
$ celery -A digital_journal worker -l info
```

Run celery beat scheduler on a new (fourth) terminal

```
$ celery -A digital_journal beat -l info
>>>>>>> email_reminders
```

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*

## Sources
The packages used by this application are specified in `requirements.txt`

*Declare are other sources here, and remove this line*
