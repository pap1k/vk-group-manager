class FieldType:
    TEXT = "TEXT"
    INT = "INT"

class Field:
    name = []
    type = []
    notNull = False
    default = ""

    def __init__(self, fieldType : FieldType, fieldName: str, fieldDefault, notNull = False, PK = False, AI = False) -> None:
        self.name = fieldName

class Table:
    Name: str = ""
    Fields: list[Field] = []