"""

author: hty / zby
create: 2015.12.07
module.py -- module exception (No such ModuleException)

"""


class ModuleException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
