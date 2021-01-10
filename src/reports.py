import asyncio
from databaseconnect import Connection


class Reports:
    def get_reports(self, user):
        connection = Connection.Instance()
        users_ref = connection.getPrimaryDatabase().collection('users')
        docs = users_ref.document(user).collection('quiz_results').stream()
        reports = []
        for doc in docs:
            reports.append({
                'datetime': doc.id,
                'score': doc.to_dict()['score']
            })

        return reports

    def get_report_for_date(self, user, datetime):
        connection = Connection.Instance()
        users_ref = connection.getPrimaryDatabase().collection('users')
        doc = users_ref.document(user).collection('quiz_results').document(datetime).get()
        return doc.to_dict()
