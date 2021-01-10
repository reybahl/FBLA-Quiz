from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from databaseconnect import Connection

class IntelligentHelpNaiveBayesClassifier:
    def classify(self, question):
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