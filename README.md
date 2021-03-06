# search-engine

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
