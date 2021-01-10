import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import asyncio
from singleton import Singleton


@Singleton
class Connection:
    def __init__(self):
        primaryCredentials = credentials.Certificate("serviceAccountKey2.json")
        primaryApp = firebase_admin.initialize_app(primaryCredentials, {
            'projectId': 'firestoredemo-2',
        }, name='primaryApp')
        self.primaryDBref = firestore.client(primaryApp)
        backupCredentials = credentials.Certificate("serviceAccountKey.json")
        backupApp = firebase_admin.initialize_app(backupCredentials, {
            'projectId': 'fir-demo-537d0',
        }, name='backupApp')
        self.backupDBref = firestore.client(backupApp)

    def getPrimaryDatabase(self):
        return self.primaryDBref

    def getBackupDatabase(self):
        return self.backupDBref

    async def update_dbref_1(self, ref, ref_type, task, data=None):
        if task == 'write':
            if ref_type == 'doc':
                ref.set(data)
        if task == 'del':
            if ref_type == 'doc':
                ref.delete()

    async def update_dbref_2(self, ref, ref_type, task, data=None):
        if task == 'write':
            if ref_type == 'doc':
                ref.set(data)
        if task == 'del':
            if ref_type == 'doc':
                ref.delete()

    async def update_both_databases(self, db1ref, db2ref, ref_type, task, data):
        # Updates both databases
        await asyncio.gather(self.update_dbref_1(db1ref, ref_type, task, data),
                             self.update_dbref_2(db2ref, ref_type, task, data))
