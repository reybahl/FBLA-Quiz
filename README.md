# FBLA Coding and Programming 2020-2021
## FBLA Randomized Quiz
*(No local installation required)*  
The application has been deployed to cloud and can be accessed directly using below link  
https://rey-fbla-quiz.herokuapp.com/


The application uses below technologies
* Python
* HTML/css
* Javascript
* Bootstrap (https://getbootstrap.com/)
* Cloud Firestore - A document oriented NoSQL database by Google (https://firebase.google.com/products/firestore).
* Firebase Authentication - Application uses firebase authentication and provides 2 options to login
  * By using email id and password
  * By using google sign-in with google account.
  * *More details on firebase authentication: https://firebase.google.com/products/auth*
* Flask - A Python web app framework. (https://palletsprojects.com/p/flask/)

## Local installation Pre-requisites
### In order to run the application locally, below are the pre-requisites
#### Softwares / Framework
* Python 3 (Python can be downloaded from here: https://www.python.org/downloads/)
* Web browser (Google chrome / Microsoft Edge / Safari (Mac OS), Mozilla Firefox


#### Python packages. (Use pip install to install the packages. Below are the commands)
There are 2 options to install packages.  
1. Using requirements.txt in this github repository. For that, please clone the project and then  
    * Go to the code root directory and run below command.
      ```
      pip install -r requirements.txt
      ```
        
      Or  
        
2. Manually install all the python packages. Use below commands
   ```
    pip install firebase-admin
    pip install textblob
    pip install pdfkit
    pip install flask
   ```
   
#### Additional dependencies
##### PDF report generation
* https://wkhtmltopdf.org/downloads.html
* *For Windows, there's an additional step needed because the wkhtmltopdf installer for windows does not update path.
    * For windows, please go to the project directory: wkhtmltopdfWindows and run batch file: wkhtmltopdfWindows.bat. This file will update the path.

## Deployment
The code internally connects to the firestore database and for that a service account key is needed. Service Account keys (for primary and backup database have been included in this repository).

Below is the format of a service account key
```
{
  "type": "service_account",
  "project_id": "project-id",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nprivate-key\n-----END PRIVATE KEY-----\n",
  "client_email": "service-account-email",
  "client_id": "client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-account-email"
}
```

The application can be run locally by using a python interpreter. Once python is installed on the local machine, please run below command.
For Windows  
```
python src\main.py
```
For MacOS Terminal or any Unix OS  
```
python src/main.py
```

The above command will start a local flask server on port 5000. Once the server starts, we can navigate to the link: http://localhost:5000 and we will reach the login page.  
New users can register using an email and password or alternately they can use Google sign-in and login by using their Google account.
