# Stack

`Server:` `gunicorn` - easy, flexible and minimalistic.

`Database:` `SQLite3` - I chose SQLite3 solution over anything else because I am lazy and noone paid me to do anything more ambitious, BUT: perfect solution would be REDIS + PostgreSQL so it is cheap, opensource, reliable and fast.

`Tests:` `django.test` - Just a simple solution, ideal solution would be pytest.

# Live version
API is hosted on [Heroku](http://intense-wildwood-04997.herokuapp.com/), so you can play with it without installing.

# Prerequisites
* Python version 3.9.0 or higher
# Start
* ```git clone https://github.com/bkpiaskun/NG_Cars_example```

* ```cd NG_Cars_example```

* ```python manage.py migrate```

* ```docker-compose build```

* ```docker-compose up```

App is running by default on port `8000`.

# Database

You don't need to have Anything installed on your device if you are using example enviroment.

If you want to use your own database yo then you should provide proper entry in ```ng/settings.py``` file. 

# NHTSA API
Application uses NHTSA to fetch information about cars.

NHTSA needs api key to work properly, by default there is no need to have any api key, so you don't need to bother about getting yours.

# Testing
It is similiar as in ``Start`` section
* ```git clone https://github.com/bkpiaskun/NG_Cars_example```

* ```cd NG_Cars_example```

* ```python manage.py test```

Keep in mind that when you run `python manage.py test` test database is used

# Environments
Settings.py file is written in that way on purpose - so you can play with application with minimal effort.
It must be changed in production environments so the app can be safe.
