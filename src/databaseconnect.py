"""FBLA Database Singleton
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>

Singleton Connection - Only one instance exists throughout the lifecycle
of the application.

Contains all the functionality related to database interaction. It connects
to firestore database https://firebase.google.com/docs/firestore
and implements a dynamic database backup feature by asynchronously
writing to two database instance, one being primary and other one being
backup.

Contains dynamic backup feature: It writes data to firestore database as the backend
and stores data in primary as well as backup database instance.

getPrimaryDatabase gets a reference to the primary database.
Returns reference to primary database

getBackupDatabase gets a reference to the backup database.
Returns reference to backup database

update_dbref_1 updates primary database.

update_dbref_2 updates backup database.

update_both_databases asynchronously updates primary and backup databases.

"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import asyncio
from singleton import Singleton


@Singleton
class Connection:
    def __init__(self):
        primaryCredentials = credentials.Certificate("src/serviceAccountKey.json")
        primaryApp = firebase_admin.initialize_app(primaryCredentials, {
            'projectId': 'firestoredemo-2',
        }, name='primaryApp')
        self.primaryDBref = firestore.client(primaryApp)
        backupCredentials = credentials.Certificate("src/serviceAccountKeyBackup.json")
        backupApp = firebase_admin.initialize_app(backupCredentials, {
            'projectId': 'fir-demo-537d0',
        }, name='backupApp')
        self.backupDBref = firestore.client(backupApp)

    def getPrimaryDatabase(self):
        """getPrimaryDatabase gets a reference to the primary database.
        :return: reference to primary database
        """
        return self.primaryDBref

    def getBackupDatabase(self):
        """getBackupDatabase gets a reference to the backup database.
        :return: reference to backup database
        """
        return self.backupDBref

    async def update_dbref_1(self, ref, ref_type, task, data=None):
        """update_dbref_1 updates primary database.
        """
        if task == 'write':
            if ref_type == 'doc':
                ref.set(data)
        if task == 'del':
            if ref_type == 'doc':
                ref.delete()

    async def update_dbref_2(self, ref, ref_type, task, data=None):
        """update_dbref_2 updates backup database.
        """
        if task == 'write':
            if ref_type == 'doc':
                ref.set(data)
        if task == 'del':
            if ref_type == 'doc':
                ref.delete()

    async def update_both_databases(self, db1ref, db2ref, ref_type, task, data):
        # Updates both databases
        """update_both_databases asynchronously updates primary and backup databases.
        """
        await asyncio.gather(self.update_dbref_1(db1ref, ref_type, task, data),
                             self.update_dbref_2(db2ref, ref_type, task, data))
