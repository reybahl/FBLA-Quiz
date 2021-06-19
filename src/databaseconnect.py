"""FBLA Database Singleton
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

import asyncio

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
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
        # Get database credentials from the service account key json generated from Firestore. This file contains the
        # private key for the primary database.
        primary_credentials = credentials.Certificate('src/serviceAccountKey.json')
        # Initialize the application object corresponding to the primary database.
        primary_app = firebase_admin.initialize_app(primary_credentials, {
            'projectId': 'firestoredemo-2',
        }, name='primary_app')
        self.primary_db_ref = firestore.client(primary_app)

        # Get database credentials from the service account key json generated from Firestore. This file contains the
        # private key for the backup database.
        backup_credentials = credentials.Certificate('src/serviceAccountKeyBackup.json')
        # Initialize the application object corresponding to the backup database.
        backup_app = firebase_admin.initialize_app(backup_credentials, {
            'projectId': 'fir-demo-537d0',
        }, name='backup_app')
        self.backup_db_ref = firestore.client(backup_app)

    def get_primary_database(self):
        """getPrimaryDatabase gets a reference to the primary database.

        :return: reference to primary database
        """
        return self.primary_db_ref

    def get_backup_database(self):
        """getBackupDatabase gets a reference to the backup database.

        :return: reference to backup database
        """
        return self.backup_db_ref

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

    async def update_both_databases(self, primary_db, backup_db, ref_type, task, data):
        """Asynchronously updates primary and backup databases.

        :param primary_db: Path to the Primary Firestore document or collection to be updated.
        :type primary_db: Object Reference
        :param backup_db: Path to the Backup Firestore document or collection to be updated.
        :type backup_db: Object Reference
        :param ref_type: Firestore document or collection
        :type ref_type: string
        :param task: Write or Delete operation
        :type task: string
        :param data: data to be written (can be new data or existing data to be updated)
        :type data: dictionary
        """
        await asyncio.gather(self.update_primary_database(primary_db, ref_type, task, data),
                             self.update_backup_database(backup_db, ref_type, task, data))
