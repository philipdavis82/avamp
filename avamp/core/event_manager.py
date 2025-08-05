from avamp.core.logging import LOG

from inspect import getframeinfo, stack
import os

class BuiltInEvents:
    FILE_SELECTED = "file_selected" 
    FILE_UNLOADED = "file_unloaded"

    DATA_SElECTED = "data_selected"

    VISUAL_READY  = "visual_selected"

class _EventManager:
    def __init__(self):
        self._event_handlers = {}

    def getCallerInfo(self):
        caller = getframeinfo(stack()[2][0])
        filename = "/".join(caller.filename.split(os.path.sep) [-2:])
        return f"{filename}[{caller.lineno}]"

    def subscribe(self, event_name, handler):
        LOG.debug(f"Registering event handler for {event_name} from {self.getCallerInfo()}")
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name].append(handler)

    def trigger(self, event_name, *args, **kwargs):
        LOG.debug(f"Triggering event {event_name} with args: {args}, kwargs: {kwargs} from {self.getCallerInfo()}")
        if event_name in self._event_handlers:
            for handler in self._event_handlers[event_name]:
                handler(*args, **kwargs)


EventManager = _EventManager()