# YaCut - educational project

### Description

The YaCut project is a link shortening service. Its purpose is to associate a long link with a short one that the user offers or provides a service.

Peculiarities of the service:

- generating short urls and linking them to the original long urls
- redirect to the original address when accessing short urls
- implemented API

### Used frameworks and libraries:
- Python 3.7
- Flask
- SQLAlchemy
- WTForms

### Template description of .env
 - FLASK_APP=yacut
 - FLASK_ENV=development
 - DATABASE_URI=sqlite:///db.sqlite3
 - SECRET_KEY=Your secret key

### How to start a project (Unix)

- Clone repository:
```bash
git clone git@github.com:ZhannaVen/yacut.git
```
- Activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
- Install dependencies:
```bash
pip install -r requirements.txt
```
- Create .env according to the template above. Be sure to change the DATABASE_URI and SECRET_KEY values
```bash
touch .env
```
- Run migrations
```bash
flask db init
flask db migrate
flask db upgrade
```
- To start a project
```bash
flask run
```

### API

- /api/id/ - POST request to create a new short link;
- /api/id/<short_id>/ — GET request to get the original link by the specified short identifier.


## Author

- [Zhanna Ventsenostseva](https://github.com/ZhannaVen)


