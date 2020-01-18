# search-engine


# Documentation
Stuff that would be nice to have in a wiki

## Installation 

### Setting up a venv and activating it

Venv tutorial - https://realpython.com/python-virtual-environments-a-primer/

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the application
tutorial - https://flask.palletsprojects.com/en/1.1.x/quickstart/

- Be in the root directory of the repository when you run these commands
- Note the setting of the FLASK_ENV variable enables debug mode
```bash
export FLASK_APP=searchapp/searchapp.py
export FLASK_ENV=development
flask run
```

## Project Structure 
Based on: 
- https://docs.python-guide.org/writing/structure/
- https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/
