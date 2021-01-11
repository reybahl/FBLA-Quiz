"""FBLA IntelligentHelp NaiveBayesClassifier
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from databaseconnect import Connection


class IntelligentHelpNaiveBayesClassifier:
    """Classifies the question category for question asked by the user
    in Get Help chat window.
    """
    def classify(self, question):
        """Gets all the training data from the database and uses that to train
        the model using :class:`textblob.classifiers.NaiveBayesClassifier` to classify the category
        of the question.
        
        :param question: question asked by the user in get help chat window
        :type question: string
        :return: Question category
        """
        connection = Connection.Instance()
        data = connection.getPrimaryDatabase().collection('intelligent_help')
        docs = data.stream()
        training_data = []
        for doc in docs:
            training_data.append((doc.to_dict()['text'], doc.to_dict()['label']))
        cl = NaiveBayesClassifier(training_data)
        text_tokens = word_tokenize(question)
        tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
        filtered_question = (" ").join(tokens_without_sw)
        return cl.classify(filtered_question)
