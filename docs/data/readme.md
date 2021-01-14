#Data Description and snapshot

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

The data itself is stored in form of a tree structure where the root of the data is a collection of questions and each question type as child document. Each question type document further contains a collection of questions. Below is how data looks like in Firestore.
