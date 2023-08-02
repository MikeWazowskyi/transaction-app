# Transaction app

## Description

#### Implementation of a simple Django RESTfull server, which make transactions between users by tax id number.

## Instructions for running

1. Clone the repository and navigate to it in the command line::

   ``` git clone https://github.com/MikeWazowskyi/transaction-app```

   ``` cd r7_test_task```

2. Create and activate a virtual environment:

   ```python -m venv venv```

   *unix:
   ```source venv/bin/activate```

   Windows:
   ```./venv/Scripts/activate```

3. Install requirements:

   ``` python -m pip install --upgrade pip```

   ``` python -m pip install -r requirements.txt```

4. Create .env file using .env_example 

5. Perform migrations:

   ``` python manage.py migrate```

6. Run application on dev server:

   ``` python manage.py runserver```

## Documentation

API documentation is available on  http://127.0.0.1:8000/docs/
