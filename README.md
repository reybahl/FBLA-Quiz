# FBLA Coding and Programming 2020-2021
## FBLA Randomized Quiz
*(No local installation required)*  
The application has been deployed to the heroku cloud and can be accessed directly using below link  
  
https://rey-fbla-quiz.herokuapp.com/  
  
*Supported Web browsers: Google chrome, Microsoft Edge, Safari (Mac OS), Mozilla Firefox*.    


#### Project API documentation
The project API has been fully documented and uploaded to the location: https://rey-fbla-quiz-docs.herokuapp.com

### About the application
#### Overview
The FBLA Quizzer application allows users to take a randomly generated quiz from a set of more than 50 questions with 5 different question types. It also stores past history of the quiz taken by any user and users can generate reports for the same.
#### Login Security
Login is safe and user information is protected.
* In order to access the application, users can either register with their email id / password or Google Sign-int.
  * For email-id/password, the application uses [Firebase Authentication](https://firebase.google.com/products/auth) and passwords are not visible to any user or administrator of the application. The passwords are stored in firebase internally and are encrypted.
  * Google Sign-in is provided by Google and users can use their Google Account to sign-in and that's very secure.
#### Data storage
**Please follow this link for details on Data: [Data Description and snapshot](docs/data/readme.md)**

* Data storage is done on [Cloud Firestore](https://firebase.google.com/products/firestore) - A document oriented NoSQL database by Google. The application supports dynamic backup feature where data is written asynchronously to a primary database instance and a backup database instance.
* Dataset contains more than [50 questions of 5 different types](docs/data/readme.md) (True/False, Fill in the blanks, Matching, Dropdown, Multiple Choice).

##### Security
Data storage is secure and protected by firestore IAM policies. No user of the application can directly modify the data and has access only to the data that belongs to the user. Only a service account or an admin can make changes to the data. Further details can be found here: [IAM](https://cloud.google.com/firestore/docs/security/iam)

### Technologies used
The application uses below technologies
* Python
* HTML/css
* Javascript
* [Bootstrap](https://getbootstrap.com/)
* [Cloud Firestore](https://firebase.google.com/products/firestore) - A document oriented NoSQL database by Google.
* [Firebase Authentication](https://firebase.google.com/products/auth) - Application uses firebase authentication and provides 2 options to login
  * By using email id and password
  * By using google sign-in with google account.
* [Flask](https://palletsprojects.com/p/flask/) - A Python web app framework.
* [Sphinx](https://www.sphinx-doc.org/en/master/) for code API documentation.
* [Heroku](https://www.heroku.com/) for cloud deployment.

## Local installation Pre-requisites
### In order to run the application locally, below are the pre-requisites
#### Softwares / Framework
* [Python 3](https://www.python.org/downloads/)
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
   
#### Additional dependency for PDF report generation
* [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)
* *For Windows, there's an additional step needed because the wkhtmltopdf installer for windows does not update path.*
    * For windows, please go to the project directory: wkhtmltopdfWindows and run batch file: wkhtmltopdfWindows.bat. This file will update the path.

### Deployment
#### Cloud
Application has been deployed to the heroku cloud and can be accessed here: https://rey-fbla-quiz.herokuapp.com/
#### Local deployment
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

#### Application Usage
* At login screen, users first need to register (if not already registered) and then enter their email and password. Alternatively they can also use their Google Account to sign-in. They can also reset their password in case they forget. For reset, they will need to enter the email id that was used to register and on clicking reset, an email will be sent to the user where they can click on a link and reset their password. Users also have the option to Continue as a guest if they want to try out the application first.
* When user logs in, there is a help page that gives instructions on how to get started and navigate
* Users can then continue to "Take a quiz tab". The application keeps track of the users' quiz progress and saves it in the database. Users may leave to another tab or even close the browser and when they come back and if they have a quiz in progress, they can resume existing quiz or take a new quiz.
* Reports tab shows the past quiz taken by the user and also provides links to generate report for each quiz.
   * Reports are generated in PDF file format using wkhtmltopdf library
   * Output reports are customizable and users can set their preferences in Settings tab
#### Futher Application Help
##### Intelligent Q&A
The application features an intelligent help feature which users can use at any time while they are on the portal. Its a chat feature where users can type a question and get answers instantly. Application internally uses [Naive Bayes classifier using textblob](https://textblob.readthedocs.io/en/dev/classifiers.html) to classify what category the question falls in and based upon that it returns the corrresponding help related to that category. The categories and corresponding help is stored in the database. Further details on Naive 
##### FAQs and Tooltip
* In the application portal, when users hover over the UI elements, there are tooltips available that provide information about the element.
* There's a tab for FAQs as well, which contains question and answers on most frequently asked questions.


## Further recommended softwares
* IDE for debugging: [Visual Studio Code](https://code.visualstudio.com/)
* IDE for debugging: [Pycharm](https://www.jetbrains.com/pycharm/)
* [Postman](https://www.postman.com/downloads/) for sending HTTP requests 
* Google Chrome browser for debugging Javascript
