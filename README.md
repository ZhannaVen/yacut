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
- The parser is launched from the ./src/
```bash
python src/main.py --help
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


