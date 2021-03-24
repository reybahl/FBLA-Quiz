"""FBLA Reports
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

import asyncio
from databaseconnect import Connection
import datetime


class Reports:
    """Contains all the functionality related to getting past quiz history
    for a user to be used for the purpose of report generation.
    """
    def get_reports(self, user):
        """Gets all the past quiz results for a user from the database to be used for 
        the purpose of report generation.

        :param user: user email for which we want to get the data
        :type user: string
        :return: A list of all the quiz results to be used for reporting purpose.
        """
        connection = Connection.Instance()
        users_primary_ref = connection.get_primary_database().collection('users')

        user_quizResults_docs = users_primary_ref.document(user).collection('quiz_results').stream()
        reports = []
        
        for doc in user_quizResults_docs:
            reports.append({
                'datetimeVal': datetime.datetime.strptime(doc.id, '%b %d %Y %I:%M%p'),
                'datetime': doc.id,
                'score': doc.to_dict()['score'],
                'timeTaken': doc.to_dict()['timetaken']
            })
        
        reports = sorted(reports, key = lambda i: i['datetimeVal'],reverse=True) #Sorts the reports based upon date and time submitted
        return reports

    def get_report_for_date(self, user, datetime):
        """Gets all the past quiz results for a user for a particular date 
        from the database to be used for the purpose of report generation.

        :param user: user email for which we want to get the data.
        :type user: string
        :param datetime: date time for when we want to get the data.
        :type datetime: string.
        :return: A list of all the quiz results to be used for reporting purpose.
        """
        connection = Connection.Instance()
        users_primary_ref = connection.get_primary_database().collection('users')
        doc = users_primary_ref.document(user).collection('quiz_results').document(datetime).get()
        return doc.to_dict()
