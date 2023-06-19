from product.Common.commandType import CommandType as Ct


class Command:
    def __init__(self, cmd=Ct.cmdInit, data='0', count=0):
        self.command = cmd
        self.data = data
        self.count = count
