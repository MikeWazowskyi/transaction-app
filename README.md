# Transaction app
[![Django CI](https://github.com/MikeWazowskyi/transaction_app/actions/workflows/django.yml/badge.svg)](https://github.com/MikeWazowskyi/transaction_app/actions/workflows/django.yml)

## Description

#### Implementation of a simple Django RESTfull server, which make transactions between users by tax id number.

## Instructions for running

1. Clone the repository and navigate to it in the command line::

   ``` git clone https://github.com/MikeWazowskyi/transaction_app.git```

   ``` cd transaction_app```

2. Create and activate a virtual environment:

   ```python -m venv venv```

   *unix:
   
   ```source venv/bin/activate```

   Windows:
   
   ```./venv/Scripts/activate```

4. Install requirements:

   ``` python -m pip install --upgrade pip```

   ``` python -m pip install -r requirements.txt```

5. Create .env file using .env_example in ./transaction-app dir

6. Perform migrations:

   ``` python manage.py migrate```

7. Run application on dev server:

   ``` python manage.py runserver```

## Documentation

API documentation is available on  http://<host>:<port>/docs
