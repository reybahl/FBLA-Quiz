"""FBLA IntelligentHelp NaiveBayesClassifier
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

from textblob.classifiers import NaiveBayesClassifier
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from databaseconnect import Connection


class IntelligentHelpNaiveBayesClassifier:
    """Classifies the question category for question asked by the user
    in Get Help chat window.
    """

    def __init__(self):
        """Checks if the required NLTK(Natural Language Toolkit) 
        data is downloaded, and if not, downloads them
        """
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

        try:
            nltk.data.find('stopwords')
        except LookupError:
            nltk.download('stopwords')

    def classify(self, question):
        """Gets all the training data from the database and uses that to train
        the model using :class:`textblob.classifiers.NaiveBayesClassifier` to classify the category
        of the question.
        
        :param question: question asked by the user in get help chat window
        :type question: string
        :return: Question category
        """
        connection = Connection.Instance()
        data = connection.get_primary_database().collection('intelligent_help')

        docs = data.stream()
        training_data = []
        for doc in docs:
            training_data.append((doc.to_dict()['text'], doc.to_dict()['label']))

        classifier = NaiveBayesClassifier(training_data)
        text_tokens = word_tokenize(question)  # Tokenizes the question
        tokens_without_stopwords = [word for word in text_tokens if
                                    not word in stopwords.words()]  # Filters stopwords(very common words) from the question
        filtered_question = (' ').join(tokens_without_stopwords)
        return classifier.classify(filtered_question)
