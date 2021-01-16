"""FBLA Database Singleton
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import asyncio
from datetime import datetime
from singleton import Singleton


@Singleton
class Connection:
    """
    Singleton Connection - Only one instance exists throughout the lifecycle
    of the application.

    Contains all the functionality related to database interaction. It connects
    to firestore database https://firebase.google.com/docs/firestore
    and implements a dynamic database backup feature by asynchronously
    writing to two database instance, one being primary and other one being
    backup.

    Contains dynamic backup feature: It writes data to firestore database as the backend
    and stores data in primary as well as backup database instance.
    """
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

    async def update_primary_database(self, ref, ref_type, task, data=None):
        """Updates primary database.

        :param ref: Path to the Firestore document or collection to be updated.
        :type ref: Object reference
        :param ref_type: Firestore document or collection
        :type ref_type: string
        :param task: Write or Delete operation
        :type task: string
        :param data: data to be written (can be new data or existing data to be updated)
        :type data: dictionary
        """
        if task == 'write':
            if ref_type == 'doc':
                ref.set(data)
        if task == 'del':
            if ref_type == 'doc':
                ref.delete()

    async def update_backup_database(self, ref, ref_type, task, data=None):
        """Updates backup database.

        :param ref: Path to the Firestore document or collection to be updated.
        :type ref: Object reference
        :param ref_type: Firestore document or collection
        :type ref_type: string
        :param task: Write or Delete operation
        :type task: string
        :param data: data to be written (can be new data or existing data to be updated)
        :type data: dictionary
        """
        if task == 'write':
            if ref_type == 'doc':
                ref.set(data)
        if task == 'del':
            if ref_type == 'doc':
                ref.delete()

    async def update_both_databases(self, primaryDB, backupDB, ref_type, task, data):
        """Asynchronously updates primary and backup databases.

        :param primaryDB: Path to the Primary Firestore document or collection to be updated.
        :type primaryDB: Object Reference
        :param backupDB: Path to the Backup Firestore document or collection to be updated.
        :type backupDB: Object Reference
        :param ref_type: Firestore document or collection
        :type ref_type: string
        :param task: Write or Delete operation
        :type task: string
        :param data: data to be written (can be new data or existing data to be updated)
        :type data: dictionary
        """
        await asyncio.gather(self.update_primary_database(primaryDB, ref_type, task, data),
                             self.update_backup_database(backupDB, ref_type, task, data))
