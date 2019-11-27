# Documentation

## Running backend

- Install Pipenv
- Run `pipenv install` in project root
- Add app.py as the flask app

```
export FLASK_APP=src/app.py
```

- Run flask

```
flask run
```

## Writing UI

UI are written in `src/templates/` with [Jinja2 template engine](https://jinja.palletsprojects.com)