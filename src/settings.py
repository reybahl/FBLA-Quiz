"""FBLA Settings
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

import asyncio
from databaseconnect import Connection


class Settings:
    """Update user settings for the purpose of report generation.
    It includes various options like font size, and content to include.
    """
    def set_prefs(self, user, request):
        """Updates all the settings for a user asynchronously to both primary and backup database.
        
        :param user: email corresponding to which the settings need to be updated.
        :type user: string
        :param settings: settings object dictionary that contains the settings from UI.
        :type settings: dictionary
        """
        connection = Connection.Instance()
        settings = convert_to_dict(request)

        users_primary_ref = connection.get_primary_database().collection('users')
        users_backup_ref = connection.get_backup_database().collection('users')
        current_user_settings_primary_ref = users_primary_ref.document(user).collection('settings').document('settings')
        current_user_settings_backup_ref = users_backup_ref.document(user).collection('settings').document('settings')

        asyncio.run(connection.update_both_databases(primary_db=current_user_settings_primary_ref, backup_db=current_user_settings_backup_ref,
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
        users_primary_ref = connection.get_primary_database().collection('users')
        current_user_settings_primary_ref = users_primary_ref.document(user).collection('settings').document('settings')
        doc = current_user_settings_primary_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return default_settings

def convert_to_dict(request):
    """Converts the users responses into a dictionary, 
    the format needed for checking
    """
    d = {}
    matching_dict = {}
    for a, b in request:
        if b == 'checkbox':
            d.setdefault(b, []).append(a)
        elif "matching" in a:
            matching_dict[a.replace('matching_', '')] = b
        else:
            d.setdefault(a, []).append(b)
    d['matching'] = matching_dict
    return d