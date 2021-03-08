# IRP
Incedo Recruitment Portal is the platform where Incedo employees can raise Job IDs, create Candidate Profiles and update their details with respect to their recruitment process.

## Steps and Prerequisites for running the project
### Installing Django 

Install(using pip) by typing these commands in your terminal
```
pip install django
```
You can confirm whether its installed or not by typing 
```
django-admin --version
```

### Other modules to be installed
Install these modules
1) django_email_verification
2) pdfkit
3) resume-parser
```
pip install django_email_verification
pip install pdfkit
pip install resume-parser
```
### Resume Parser dependencies
Resume parser will need other python modules to be installed
which have been installed automatically and after it these should also need to be installed
```
pip install nltk
pip install resume-parser
pip install spacy==2.3.5
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz
```

#Note This is for JD files:
Only PDF file can be view in the browser iteself.Doc and Docx are downloadable
### Running the code 
Just make sure you are in IRP directory and type in terminal 
```
python manage.py runserver
```
"IRP" web-app will start on 127.0.0.1:8000 (Local Address).
 
### Applying Migrations on the Project 
Migrations are Django’s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. They’re designed to be mostly automatic, but you’ll need to know when to make migrations, when to run them, and the common problems you might run into.
If you want to change the models you can simply change the code in 'models.py' file in respective app as you require and then run these commands
```
python manage.py makemigrations
python manage.py migrate 
python manage.py runserver
```
You can use *showmigration*  to list projects migration.
