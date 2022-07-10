# Django-Swap-User (Beta)
![django-swap-user](https://skonik.github.io/django-swap-user-docs/media/images/django-swap-user.png)
<p align="center">
  <a href="https://github.com/artinnok/django-user-swap/actions/workflows/test.yml">
    <img alt="test" src="https://github.com/artinnok/django-user-swap/actions/workflows/test.yml/badge.svg">
  </a>
  <a href="https://github.com/skonik/django-swap-user-docs/actions/workflows/main.yml">
    <img alt="docs" src="https://github.com/skonik/django-swap-user-docs/actions/workflows/main.yml/badge.svg">
  </a>
  <a href="https://pypi.org/project/django-swap-user/" target="_blank">
    <img src="https://img.shields.io/badge/pypi-v0.9.8-green" alt="PyPi">
  </a>
</p>


If you are tired of copying one custom user model from one project to another - use this package.
This will do it all for you.

## Documentation
All official documentation hosted [here](https://skonik.github.io/django-swap-user-docs/).

## Installation
```
pip install django-swap-user
```

## Basic usage
1. Choose a model that suits you and copy related settings from the table:

| Application name | Username field | Description                                                            | `INSTALLED_APPS`                               | `AUTH_USER_MODEL`                      | Replace `django.contrib.admin` to          |
|------------------|----------------|------------------------------------------------------------------------|------------------------------------------------|----------------------------------------|--------------------------------------------|
| `to_email`       | `email`        | User with `email` username                                             | ```"swap_user", "swap_user.to_email",```       | `"swap_to_email.EmailUser"`            | not required                               |                                  
| `to_email_otp`   | `email`        | User with `email` username, without `password` and OPT authentication  | ```"swap_user", "swap_user.to_email_otp",```   | `"swap_to_email_otp.EmailOTPUser"`     | `"swap_user.apps.OTPSiteConfig"`           |
| `to_phone`       | `phone`        | User with `phone` username                                             | ```"swap_user", "swap_user.to_phone",```       | `"swap_to_phone.PhoneUser"`            | not required                               |                                            
| `to_phone_otp`   | `phone`        | User with `phone` username, without `password`  and OTP authentication | ```"swap_user", "swap_user.to_phone_otp",```   | `"swap_to_phone_otp.PhoneOTPUser"`     | `"swap_user.apps.OTPSiteConfig"`           |

2. Add corresponding app to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    "swap_user",
    "swap_user.to_email",
    ...
]
```

3. Change `AUTH_USER_MODEL` to corresponding:
```python
AUTH_USER_MODEL = "swap_to_email.EmailUser"
```

4. If required replace `django.contrib.admin` in `INSTALLED_APPS` to something.

5. Apply migrations:
```bash
python manage.py migrate swap_to_email
```


## Architecture
Application `swap_user` split into 3 apps:
  - `to_email` - provides user with `email` username field
  - `to_email_otp` - provides user with `email` username field and OTP (One Time Password) authentication
  - `to_phone` - provides user with `phone` username field
  - `to_phone_otp` - provides user with `phone` username field and OTP (One Time Password) authentication
  
  
## Why the unusual architecture?
Because if we leave them in one app, they all will create migrations and tables - such approach leads us to redundant tables.
They will be treated as 3 custom models within the same app, which causes perplexing and cognitive burden.

With such approach (when there is a common app which contains internal apps) - the user 
can choose to connect with the specific user model which is most applicable for concrete business-logic. 

I have found such approach at Django REST Framework `authtoken` application and decide to use it - reference is [here](https://github.com/encode/django-rest-framework/tree/master/rest_framework/authtoken).


## Providing User model at start of project
When you are starting a project from zero or scratch - this is a best moment to provide custom User model.
Because you have't a lot of migrations or you can easily regenerate them. Moreover, Django's [official docs](https://docs.djangoproject.com/en/dev/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project)
recommend to provide custom User model even if you are fully satisfied with default one - in future it will be easier to extend custom model that fits into your business cases.


## Providing User model at mid of project
This is a harder way of doing things, but it is still possible to do:
- Do all the steps at testing database and ONLY IF all of them was successful - try to apply at production environment
- Please note that these steps are **common** - they fit in most cases, but in some circumstances you need act on situation.
- Create a backup of your database
- Add stable tag into your repository or save a commit hash reference
- Pray to the heavens
- Remove all of yours migrations in every app of Django's project
- Remove all records from `django_migrations` table, for example with SQL `TRUNCATE django_migrations`
- Now we have a "clean" state, so we can change default model
- Generate new migrations for all of your applications - `python manage.py makemigrations` 
- Now we need to [fake migrate](https://docs.djangoproject.com/en/4.0/ref/django-admin/#cmdoption-migrate-fake) because we already have all the tables with data
- First fake the `auth` application because we are depending from this one - `python manage.py migrate --fake auth`
- Install this library, follow instructions and apply migrations
- Then fake rest of migrations we have - `python manage.py migrate --fake`
- Run your application!


## Development
If you want to contribute in this project please consider the following instruction.

### Project setup for development

1. `poetry install` to install poetry deps;

2. `pre-commit install` to install git hooks;


### Commands useful in development
You can execute a bunch of useful commands located inside `Makefile`:

* `make lint` - run code quality tools such as flake8, isort, safety;
* `make format` - format your code using black and isort;
* `make test` - run tests;


### Sponsor
[django-swap-user](https://evrone.com/django-swap-user?utm_source=github&utm_medium=django-swap-user) project is created & supported by [Evrone](https://evrone.com?utm_source=github&utm_medium=django-swap-user)

[<img src="https://evrone.com/logo/evrone-sponsored-logo.png" width=300>](https://evrone.com?utm_source=github&utm_medium=python-guidelines)

