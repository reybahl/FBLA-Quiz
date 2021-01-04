# FBLA Coding and Programming 2020-2021
## FBLA Randomized Quiz
This repository contains code for FBLA coding and programming competitive events 2020-2021. The application uses below technologies
* Python
* HTML/css
* Javascript
* Cloud Firestore - A document oriented NoSQL database by Google.
* Firebase Authentication - Application uses firebase authentication and provides 2 options to login
  * By using email id and password
  * By using google sign-in with google account.
* Flask - A Python web app framework.

## Pre-requisites
### In order to run the application, below are the pre-requisites
#### Softwares / Framework
* Python 3
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

The above command will start a local flask server on port 5000.Once the server starts, we can navigate to the link: http://localhost:5000 and we will reach the login page.  
New users can register using an email and password or alternately they can use Google sign-in and login by using their gmail account.
