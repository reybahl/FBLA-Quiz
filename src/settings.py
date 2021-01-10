import asyncio
from databaseconnect import Connection


class Settings:
    def set_prefs(self, user, settings):
        connection = Connection.Instance()
        users_ref = connection.getPrimaryDatabase().collection('users')
        users_ref2 = connection.getBackupDatabase().collection('users')
        current_user_settings_ref = users_ref.document(user).collection('settings').document('settings')
        current_user_settings_ref2 = users_ref2.document(user).collection('settings').document('settings')

        asyncio.run(
            connection.update_both_databases(db1ref=current_user_settings_ref, db2ref=current_user_settings_ref2,
                                             ref_type='doc', task='write', data={'settings': settings}))

    def get_prefs(self, user):
        connection = Connection.Instance()
        default_settings = {
            'settings': {
                'Name': [''],
                'font': ['18'],
                'Username': [user],
                'checkbox': ['showwronganswer', 'score', 'q_number']
            }
        
        #By default, reports will have 18 px font, and will include the correct answer for incorrectly answered questions, the score, and question numbers
        }
        users_ref = connection.getPrimaryDatabase().collection('users')
        current_user_settings_ref = users_ref.document(user).collection('settings').document('settings')
        doc = current_user_settings_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return default_settings
