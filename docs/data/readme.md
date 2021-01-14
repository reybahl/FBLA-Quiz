# Data Description and snapshot

Dataset contains more than 50 questions of 5 different types
* True/False
* Fill in the blanks
* Matching
* Dropdown
* Multiple Choice
  * Questions with one answers (shown in form of a radio button)
  * Questions with multiple answers (shown in form of check boxes to select multiple)

Data is persistently stored in [Cloud Firestore](https://firebase.google.com/products/firestore), a document oriented NoSQL database by Google. The application supports dynamic backup feature where data is written asynchronously to a primary database instance and a backup database instance.

Below is a screenshot of how primary and backup database look like in firestore.

![alt text](screenshots/primary_backup.png)

The data itself is stored in form of a tree structure where the root of the data is a collection of questions and each question type as child document. Each question type document further contains a collection of questions. 

Below is how sample data looks like for multiple choice questions in Firestore.

Questions By Type
![alt text](screenshots/questions_by_type.png)

Questions
![alt text](screenshots/questions.png)
The document in the extreme right in the above image contains an actual question. "options" represents all the options that would be presented to the user. "answers" represents the correct answers.

## Dataset
Below is complete dataset extracted from firestore in JSON format.

