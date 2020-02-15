# search-engine

# Instructions for the Grader
Assumptions prior to install
- Python 3 and Pip3 is installed and accessible from the command line

# Table of Contents
- Installation
    - Dependencies
    - Automated installation of external dependencies with pip and virtualenv (Optional)
- Running the application
    - Powershell Instructions
    - CMD Instructions
- Rebuilding the Index with Stopword, Stemming and Normalization toggled

## Installation 
#### Dependencies
- The following list is the list of external dependencies that you may manually install. Alternatively you may follow the instructions **Installing external dependencies with pip and requirements.txt** for an automated installation. 
```
beautifulsoup4==4.8.2
Click==7.0
Flask==1.1.1
itsdangerous==1.1.0
Jinja2==2.10.3
lxml==4.4.2
MarkupSafe==1.1.1
nltk==3.4.5
numpy==1.18.1
pandas==1.0.1
pip-autoremove==0.9.1
python-dateutil==2.8.1
pytz==2019.3
six==1.14.0
soupsieve==1.9.5
weighted-levenshtein==0.2.1
Werkzeug==0.16.0
```

#### Installing external dependencies with pip and requirements.txt 

Run the following commands
```
py -3 -m venv venv
venv\Scripts\activate
pip3 install -r requirements.txt
```

If you encounter the following error or something similar:
```
venv\Scripts\activate : File C:\Users\Raymo\Desktop\blah\search-engine\venv\Scripts\Activate.ps1 cannot be
loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies
at https:/go.microsoft.com/fwlink/?LinkID=135170.
At line:1 char:1
+ venv\Scripts\activate
+ ~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```
1. Open PowerShell in Administrator mode
2. Input this in the prompt
```
set-executionpolicy remotesigned
```
3. Say yes

Reference: https://superuser.com/questions/106360/how-to-enable-execution-of-powershell-scripts

## Running the application

- **Be in the root directory of the repository when you run these commands**
- The contents of the folder you are in should be:
```
env.sh  index.log  Makefile  README.md  requirements.txt  searchapp/  tests/  venv/
```
- You may use either PowerShell or CMD

##### Powershell Instructions
Run the following commands
```
$env:FLASK_APP = "searchapp/searchapp.py"
flask run
```
##### OR
##### CMD Instructions
Run the following commands
```
set FLASK_APP=searchapp/searchapp.py
flask run
```
Reference - https://flask.palletsprojects.com/en/1.1.x/quickstart/

## Rebuilding the Index with Stopword, Stemming and Normalization toggled
- The file searchapp/searchapp.py contains the code snippet (Line 23):
```{python}
# README: Change booleans here to toggle stopword, stemming and normalization respectively
inverIndex = indexAndDictBuilder.buildIndex("searchapp/cor_pre_proc/corpus", True, True, True)
```
1. Modify the Boolean parameters to toggle: Stopword, Stemming and Normalization respectively as stated in the code snippet
2. Rerun the application using the instructions found in the previous section **Running the application**
3. The inverted index is stored in a file named *index.json*. The Bigram index is stored in a file named *biIndex.json*.
    - These files are located in searchapp/index_and_dict/
# End of Instructions for the Grader

# Developer Instructions

## Installation 
Assumptions prior to install
- Python 3 is installed and accessible from the path

### Setting up a venv and activating it
- Reference: https://realpython.com/python-virtual-environments-a-primer/

#### Linux instructions
Run the following commands
- Note that if you are using the fish shell to use "activate.fish" instead of "activate"
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows instructions
Run the following commands
```
py -3 -m venv venv
venv\Scripts\activate
pip3 install -r requirements.txt
```

If you encounter the following error or something similar:
```
venv\Scripts\activate : File C:\Users\Raymo\Desktop\blah\search-engine\venv\Scripts\Activate.ps1 cannot be
loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies
at https:/go.microsoft.com/fwlink/?LinkID=135170.
At line:1 char:1
+ venv\Scripts\activate
+ ~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```
1. Open PowerShell in Administrator mode
2. Input this in the prompt
```
set-executionpolicy remotesigned
```
3. Say yes

Reference: https://superuser.com/questions/106360/how-to-enable-execution-of-powershell-scripts

### Deactivating a venv
Run the following command
```
deactivate
```

### Viewing installed packages
- You can see your installed requirements from pip using the command
```bash
pip freeze
```

## Running the application
Reference - https://flask.palletsprojects.com/en/1.1.x/quickstart/

- Be in the root directory of the repository when you run these commands
- Note the setting of the FLASK_ENV variable enables debug mode
    - **The indexes and corpus will NOT be rebuilt when development mode is set**

#### Linux instructions
Run the following commands
```bash
export FLASK_APP=searchapp/searchapp.py
export FLASK_ENV=development
flask run
```

#### Windows instructions

##### Powershell Instructions
Run the following commands
```
$env:FLASK_APP = "searchapp/searchapp.py"
$env:FLASK_ENV = "development"
flask run
```
##### CMD Instructions
Run the following commands
```
set FLASK_APP=searchapp/searchapp.py
set FLASK_ENV=development
flask run
```

## Project Structure 
Based on: 
- https://docs.python-guide.org/writing/structure/
- https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/
