from naivebayesclassifier import IntelligentHelpNaiveBayesClassifier
from databaseconnect import Connection


class IntelligentQA:
    def get_help(self, question_json):
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
