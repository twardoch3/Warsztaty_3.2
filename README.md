# Warsztaty_3.2 - Django Basics Module - Contact Box Application
Application allows to manage contacts (add, edit or delete people and their addresses, emails and phone numbers).

[Deployed version](https://contact-box123.herokuapp.com/)

### Requirements
Program requires PostgreSQL database and Django.

### Installing
Create database 'cbox_db' with tables for contact people. Install requirements  with command:
```
pip install -r requirements.txt
```
### Running the program
Apply the migrations:
```
python manage.py migrate
```
Start a development Web server on the local machine with command:
```
python manage.py runserver
```

### Usage Examples:
Create person:
```
http://127.0.0.1:8000/person/new/
```
Create contact:
```
http://127.0.0.1:8000/contact/new/
```

