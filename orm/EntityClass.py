from orm.Types import *
import inspect

def getType(t):
        t = type(t[1])
        if t == int:
            return FieldType.INT
        if t == str:
             return FieldType.TEXT

class Entity:
    _dbTable : Table = None
    def __new__(cls):
        for i in inspect.getmembers(cls):
            if not i[0].startswith('_'):  
                if not inspect.ismethod(i[1]):
                     print(getType(i))

    