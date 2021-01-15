"""FBLA IntelligentQA
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

from naivebayesclassifier import IntelligentHelpNaiveBayesClassifier
from databaseconnect import Connection


class IntelligentQA:
    """Contains all the functionality related to intelligent help. 
    Contains dynamic backup feature: It writes data to firestore database as the backend
    and stores data in primary as well as backup database instance.
    """
    def __init__(self):
        """Initializes object and creates a Naive Bayes Classifier object
        """
        self.intelligentHelpNaivebayesclassifier = IntelligentHelpNaiveBayesClassifier()

    def get_help(self, question_json):
        """Intelligent Q&A feature: This gets called when user types a
        question in get help chat window. It uses Naive Bayes algorithm
        to classify what category the question falls in and based upon that
        it returns the corrresponding help related to that category. The
        categories and corresponding help is stored in the database.

        :param question_json: question asked by the user in get help chat window
        :type question_json: JSON string

        :return: List of questions and answers corresponding to category of the 
                question that user has asked.
        """
        classification = self.intelligentHelpNaivebayesclassifier.classify(question_json['question'])
        connection = Connection.Instance()
        q_a_list_fromDatabase = connection.getPrimaryDatabase().collection('help').document(classification).collection('Q&A').stream()
        q_a_list = []

        for doc in q_a_list_fromDatabase:
            qa = doc.to_dict()
            q_a_list.append(qa)

        return q_a_list

    def get_frequently_asked_questions(self):
        """Get the list of all the faqs from the database.
        :return: List of questions and answers.
        """
        questions = []
        connection = Connection.Instance()
        help_questions_answers = connection.getPrimaryDatabase().collection('help')
        docs = help_questions_answers.stream()

        for doc in docs:
            category = doc.id
            questions_of_category = help_questions_answers.document(category).collection('Q&A').stream()
            
            for question in questions_of_category:
                questions.append({'question': question.to_dict()['question'],
                                  'answer': question.to_dict()['answer']})
        return questions