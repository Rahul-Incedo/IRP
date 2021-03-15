# IRP
Incedo Recruitment Portal is the platform where Incedo employees can raise Job IDs, create Candidate Profiles and update their details with respect to their recruitment process.

## Steps and Prerequisites for running the project

### Installing Python and Java
Python version-3.9 is used (pip should be installed with python setup)  
Java version-1.8.0 is used with this project  

### Installing Django
Install(using pip) by typing these commands in your terminal
```
pip install django==3.1.7
```
You can confirm whether its installed or not by typing 
```
django-admin --version
```

### Other modules to be installed
Install these modules
1) django_email_verification
2) pdfkit
3) jsonfield
4) resume-parser
```
pip install django_email_verification
pip install pdfkit
pip install jsonfield
pip install resume-parser
```
### Resume Parser dependencies
Resume parser will need these python modules to be installed additionally for proper functioning  
Refer this link for more info - https://pypi.org/project/resume-parser/  
Note: make sure to install spacy with the given version (newer versions are not supported with the resume-parser module)
#### spaCy
```
pip install spacy==2.3.5
python -m spacy download en_core_web_sm
```
#### nltk
```
pip install nltk
python -m nltk.downloader stopwords
python -m nltk.downloader punkt
python -m nltk.downloader averaged_perceptron_tagger
python -m nltk.downloader universal_tagset
python -m nltk.downloader wordnet
python -m nltk.downloader brown
python -m nltk.downloader maxent_ne_chunker
```
#### Note : For extracting .doc resume files  
Resume parser need java to be installed at the serverside to operate on .doc files

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

#### Note:Check once with resume parsed value because its accuracy is not high

#### Note : For opening files in the browser itself
Only .pdf files can be viewed directly in the browser iteself .doc and .docx need additional browser extension for viewing directly , although you can dowload and open the files

##Note: Make sure that whether you installed JDK on your machine(Java) to start tika server
