# CongoCart
A simple B2B E-Commerce web application to provide advantages of online shopping to retailers and wholesalers. 

## Getting Started

### Clone the repository
Clone the repository and change to project root directory (where manage.py file is).
```
$ git clone git@github.com:bshukla3041/CongoCart.git
$ cd CongoCart
```
### Install the dependencies
* Create a virtual environment with python3 and pip3 (recommended).
* Install required python dependencies. 
  ```
    pip3 install -r requirements.txt
  ```
* Get your own Stripe API Keys (test keys) and update STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY variable in settings.py file. Follow ```https://testdriven.io/blog/django-stripe-tutorial/#add-stripe``` to get test API keys.

### Run the application
* Run the application by starting the local server from project root directory.
  ```
    python3 manage.py runserver
  ```
* Access the application in your browser at http://localhost:8000
* Live Demo of this application is hosted at https://congocart.pythonanywhere.com/

### License
CongoCart is distributed under the MIT License. 
