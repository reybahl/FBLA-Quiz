"""FBLA IntelligentQA
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

from naivebayesclassifier import IntelligentHelpNaiveBayesClassifier
from databaseconnect import Connection


class IntelligentQA:
    """Contains all the functionality related to quiz. 
    Contains dynamic backup feature: It writes data to firestore database as the backend
    and stores data in primary as well as backup database instance.
    """
    def get_help(self, question_json):
        """Intelligent Q&A feature: This gets called when user types a
        question in get help chat window. It uses Naives Bayes algorithm
        to classify what category the question falls in and based upon that
        it returns the corrresponding help related to that category. The
        categories and corresponding help is stored in the database.

        :param question_json: question asked by the user in get help chat window
        :type question_json: JSON string

        :return: List of questions and answers corresponding to category of the 
                question that user has asked.
        """
        intelligentHelpNaivebayesclassifier = IntelligentHelpNaiveBayesClassifier()
        classification = intelligentHelpNaivebayesclassifier.classify(question_json['question'])
        connection = Connection.Instance()
        qas = connection.getPrimaryDatabase().collection('help').document(classification).collection('Q&A').stream()
        qaarr = []
        for doc in qas:
            qa = doc.to_dict()
            qaarr.append(qa)
        return qaarr

    def get_frequently_asked_questions(self):
        """Get the list of all the faqs from the database.
        :return: List of questions and answers.
        """
        questions = []
        connection = Connection.Instance()
        qa = connection.getPrimaryDatabase().collection('help')
        docs = qa.stream()
        for doc in docs:
            category = doc.id
            questions_of_category = qa.document(category).collection('Q&A').stream()
            for question in questions_of_category:
                questions.append({'question': question.to_dict()['question'],
                                  'answer': question.to_dict()['answer']})
        return questions
