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
```

## Sources
The packages used by this application are specified in `requirements.txt`
