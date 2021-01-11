# FBLA Coding and Programming 2020-2021
## FBLA Randomized Quiz
*(No local installation required)*  
The application has been deployed to cloud and can be accessed directly using below link  
https://rey-fbla-quiz.herokuapp.com/


The application uses below technologies
* Python
* HTML/css
* Javascript
* Cloud Firestore - A document oriented NoSQL database by Google (https://firebase.google.com/products/firestore).	
* Firebase Authentication - Application uses firebase authentication and provides 2 options to login	
  * By using email id and password	
  * By using google sign-in with google account.
  * *More details on firebase authentication: https://firebase.google.com/products/auth*
* Flask - A Python web app framework. (https://palletsprojects.com/p/flask/)

## Local installation Pre-requisites
### In order to run the application, below are the pre-requisites
#### Softwares / Framework
* Python 3 (Python can be downloaded from here: https://www.python.org/downloads/)
* Web browser (Google chrome / Microsoft Edge / Safari (Mac OS), Mozilla Firefox


#### Python packages. (Use pip install to install the packages. Below are the commands)
* pip install firebase-admin
* pip install textblob
* pip install pdfkit
* pip install flask

#### Additional dependencies
##### PDF report generation
* https://wkhtmltopdf.org/downloads.html

## Deployment
The application can be run locally by using a python interpreter. Once python is installed on the local machine, please run below command.  
* python3 main.py.

The above command will start a local flask server on port 5000. Once the server starts, we can navigate to the link: http://localhost:5000 and we will reach the login page.  
New users can register using an email and password or alternately they can use Google sign-in and login by using their Google account.
