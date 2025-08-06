from inspect import getframeinfo, stack
import os
class _Logger:
    def __init__(self, name):
        self.name = name
        self.logs = []
    
    def getCallerInfo(self):
        caller = getframeinfo(stack()[3][0])
        filename = "/".join(caller.filename.split(os.path.sep) [-2:])
        return f"{filename}[{caller.lineno}]"

    def getPreamble(self,level:str):
        return f"{level:5s}: {self.getCallerInfo()}"

    def debug(self, message):
        log_entry = f'{self.getPreamble("DEBUG"):50s}: {message}'
        self.logs.append(log_entry)
        print(log_entry)
    def info(self, message):
        log_entry = f'{self.getPreamble("INFO"):50s}: {message}'
        self.logs.append(log_entry)
        print(log_entry)
    def warning(self, message):
        log_entry = f'{self.getPreamble("WARN"):50s}: {message}'
        self.logs.append(log_entry)
        print(log_entry)
    def error(self, message):
        log_entry = f'{self.getPreamble("ERROR"):50s}: {message}'
        self.logs.append(log_entry)
        print(log_entry)
    def critical(self, message):
        log_entry = f'{self.getPreamble("FATAL"):50s}: {message}'
        self.logs.append(log_entry)
        print(log_entry)

LOG = _Logger("Log")