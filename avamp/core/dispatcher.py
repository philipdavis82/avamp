from avamp.core.logging import LOG
from avamp.core.event_manager import EventManager, BuiltInEvents

class _VisualDispatcher:
    activeVisuals: list[object]
    registeredVisuals: dict[str, list[object]]
    def __init__(self):
        LOG.debug("VisualDispatcher initialized")
        # Subscribe to events
        EventManager.subscribe(BuiltInEvents.DATA_SElECTED, self.on_data_selected)

        self.activeVisuals     = []
        self.registeredVisuals = {}


    def on_data_selected(self, data, filename):
        LOG.debug(f"Data selected from {filename}: {data.type()}:{data.name()}")
        if data.type() in self.registeredVisuals:
            for visual in self.registeredVisuals[data.type()]:
                LOG.debug(f"Notifying visual {visual} of data selection")
                EventManager.trigger(
                    BuiltInEvents.VISUAL_READY,
                    visual=visual,
                    data=data,
                    filename=filename
                )
        else:
            LOG.warning(f"No registered visuals for data type: {data.type()}")

    def add_visual(self, visual:object, type:str):
        LOG.debug(f"Adding visual of type {type}: {visual}")
        if type not in self.registeredVisuals:
            self.registeredVisuals[type] = []
        self.registeredVisuals[type].append(visual)
        LOG.debug(f"Visual of type {type} added. Total visuals: {len(self.registeredVisuals[type])}")

VisualDispatcher = _VisualDispatcher()