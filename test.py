from orm import Entity, Types
from log import Log

logger = Log("[TEST]").log



class Test:
    def __init__(self):
        x = []
        x + 1
        logger("гамарджоба")

try:
    t = Test()
except Exception as e:
    logger(f"Ошибка {e}",isCrash=True)
# t = Test()