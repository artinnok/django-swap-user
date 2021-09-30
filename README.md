# Django-Swap-User (Beta)

## About
If you are tired from copying one custom user model from one project to another ones - use this package.
This will do all for you. 


## Installation
```
pip install django-swap-user
```

## Basic usage
1. Choose one of models and settings from table:

| Application name | Username field | Description                                                           | INSTALLED_APPS                           | AUTH_USER_MODEL                 |
|------------------|----------------|-----------------------------------------------------------------------|------------------------------------------|---------------------------------|
| to_email         | "email"        | User with `email` username                                            | "swap_user", "swap_user.to_email",       | "to_email.EmailUser"            |
| to_named_email   | "email"        | User with `email` username, `first_name` and `last_name` extra fields | "swap_user", "swap_user.to_named_email", | "to_named_email.NamedEmailUser" |
| to_phone         | "phone"        | User with `phone` username                                            | "swap_user", "swap_user.to_phone",       | "to_phone.PhoneUser"            |

2. Add corresponding app to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    "swap_user",
    "swap_user.to_named_email",
    ...
]
```
3. Change `AUTH_USER_MODEL` to corresponding:
```python
AUTH_USER_MODEL = "to_named_email.NamedEmailUser"
```


## Architecture
Application `swap_user` split into 3 apps:
  - `to_email` - provides user with `email` username field
  - `to_named_email` - provides user with `email` username field and with `first_name`, `last_name` extra fields
  - `to_phone` - provides user with `phone` username field
  
  
## Why?
Because if we leave them in one app, they all will create migrations and tables - such approach leads us to redundant tables.
They will be treated as 3 custom models within the same app, which causes perplexing and cognitive burden.

With such approach (when there is a common app which contains internal apps) - the user 
choose and connect only the specific user model which suits best for concrete business-logic. 

I have found such approach at Django REST Framework `authtoken` application and decide to use it - reference is [here](https://github.com/encode/django-rest-framework/tree/master/rest_framework/authtoken).
