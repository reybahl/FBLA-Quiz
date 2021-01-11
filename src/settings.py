"""FBLA Settings
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

import asyncio
from databaseconnect import Connection


class Settings:
    """Update user settings for the purpose of report generation.
    It includes various options like font size, and content to include.
    """
    def set_prefs(self, user, settings):
        """Updates all the settings for a user asynchronously to both primary and backup database.
        
        :param user: email corresponding to which the settings need to be updated.
        :type user: string
        :param settings: settings object dictionary that contains the settings from UI.
        :type settings: dictionary
        """
        connection = Connection.Instance()
        users_ref = connection.getPrimaryDatabase().collection('users')
        users_ref2 = connection.getBackupDatabase().collection('users')
        current_user_settings_ref = users_ref.document(user).collection('settings').document('settings')
        current_user_settings_ref2 = users_ref2.document(user).collection('settings').document('settings')

        asyncio.run(
            connection.update_both_databases(db1ref=current_user_settings_ref, db2ref=current_user_settings_ref2,
                                             ref_type='doc', task='write', data={'settings': settings}))

    def get_prefs(self, user):
        """Gets all the settings for a user from the primary database.
        
        :param user: email corresponding to which the settings need to be retrieved.
        :type user: string
        :return: Settings corresponding to the user
        """
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
