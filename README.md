# CongoCart
A B2B E-Commerce application

## Getting Started

### Installing
* Create a virtual environment with python3 and pip3 (recommended)
* Install required python dependencies 
  ```
    pip3 install -r requirements.txt
  ```
* Change to project root directory (where manage.py file is)
  ```
    cd CongoCart
  ```
* Get your own Stripe API Keys (test keys) and update STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY variable in settings.py file. Follow ```https://testdriven.io/blog/django-stripe-tutorial/#add-stripe``` to get test API keys.
* Run the local server from project root directory
  ```
    python3 manage.py runserver
  ```
* Access the website in your browser at ```http://localhost:8000```