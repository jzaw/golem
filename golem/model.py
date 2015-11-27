from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, FloatField, DateTimeField, CompositeKey

import datetime

DATABASE_NAME = 'golem.db'
START_BUDGET = 42000000


class SqliteFKTimeoutDatabase(SqliteDatabase):
    def initialize_connection(self, conn):
        self.execute_sql('PRAGMA foreign_keys = ON')
        self.execute_sql('PRAGMA busy_timeout = 30000')


db = SqliteFKTimeoutDatabase(DATABASE_NAME, threadlocals=True)


class Database:
    def __init__(self):
        self.db = db
        self.name = DATABASE_NAME

        db.connect()
        self.create_database()

    def create_database(self):
        db.create_tables([Node, Bank, LocalRank, GlobalRank, NeighbourLocRank], safe=True)

    def check_node(self, node_id):
        with db.transaction():
            nodes = [n for n in Node.select().where(Node.node_id == node_id)]
            if len(nodes) == 0:
                Node.create(node_id=node_id)
            bank = [n for n in Bank.select().where(Bank.node_id == node_id)]
            if len(bank) == 0:
                Bank.create(node_id=node_id)


class BaseModel(Model):
    class Meta:
        database = db


class Node(BaseModel):
    node_id = CharField(primary_key=True)
    created_date = DateTimeField(default=datetime.datetime.now)
    modified_date = DateTimeField(default=datetime.datetime.now)


class Bank(BaseModel):
    node_id = ForeignKeyField(Node, related_name='has', unique=True)
    val = FloatField(default=START_BUDGET)
    created_date = DateTimeField(default=datetime.datetime.now)
    modified_date = DateTimeField(default=datetime.datetime.now)


class LocalRank(BaseModel):
    node_id = CharField(unique=True)
    positive_computed = FloatField(default=0.0)
    negative_computed = FloatField(default=0.0)
    wrong_computed = FloatField(default=0.0)
    positive_requested = FloatField(default=0.0)
    negative_requested = FloatField(default=0.0)
    positive_payment = FloatField(default=0.0)
    negative_payment = FloatField(default=0.0)
    positive_resource = FloatField(default=0.0)
    negative_resource = FloatField(default=0.0)
    created_date = DateTimeField(default=datetime.datetime.now)
    modified_date = DateTimeField(default=datetime.datetime.now)


class GlobalRank(BaseModel):
    node_id = CharField(unique=True)
    requesting_trust_value = FloatField(default=0.0)
    computing_trust_value = FloatField(default=0.0)
    gossip_weight_computing = FloatField(default=0.0)
    gossip_weight_requesting = FloatField(default=0.0)
    created_date = DateTimeField(default=datetime.datetime.now)
    modified_date = DateTimeField(default=datetime.datetime.now)


class NeighbourLocRank(BaseModel):
    node_id = CharField()
    about_node_id = CharField()
    requesting_trust_value = FloatField(default=0.0)
    computing_trust_value = FloatField(default=0.0)
    created_date = DateTimeField(default=datetime.datetime.now)
    modified_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        primary_key = CompositeKey('node_id', 'about_node_id')