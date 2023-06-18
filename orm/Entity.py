from orm.Types import *
class Entity:
    dbTable : Table
    def __init__(self):
        pass
    def __new__(cls):
        #sql create table or alter
        pass