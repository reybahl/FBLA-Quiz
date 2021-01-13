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
        users_ref = connection.getPrimaryDatabase().collection('users')
        docs = users_ref.document(user).collection('quiz_results').stream()
        reports = []
        for doc in docs:
            reports.append({
                'datetime': doc.id,
                'score': doc.to_dict()['score']
            })
        
        reports = sorted(reports, key = lambda i: i['datetime'],reverse=True)
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
        users_ref = connection.getPrimaryDatabase().collection('users')
        doc = users_ref.document(user).collection('quiz_results').document(datetime).get()
        return doc.to_dict()
