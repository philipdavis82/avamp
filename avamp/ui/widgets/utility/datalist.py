from avamp.core.logging import LOG
from avamp.core.parsers.base_parser import BaseParser
from avamp.core.parsers import PARSERS,ACTIVE_PARSERS
from avamp.core.event_manager import EventManager, BuiltInEvents

from PyQt6.QtWidgets import QWidget, QGridLayout, QMenuBar, QTreeWidget, QTreeWidgetItem, QMenu
from PyQt6.QtCore import QObject, QEvent, QEventLoop, QPoint

import os

class RightClickedFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.ContextMenu:
            # item = obj.itemAt(event.position().toPoint())
            item = obj.itemAt(obj.getItemOffsetFromHeader(event.pos()))
            if item:
                LOG.info(f"Right-clicked on item: {item.text(0)}")
                menu = QMenu(obj)
                action = menu.addAction("Remove Item")
                action.triggered.connect(lambda: obj.clear(item.text(0)))
                menu.exec(event.globalPos())
            return True
        return super().eventFilter(obj, event)

class DataList(QTreeWidget):
    openParsers: dict[str, BaseParser]
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabels(["Name", "Type", "Size"])
        self.setColumnCount(3)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)

        # Connect to event manager
        EventManager.subscribe(BuiltInEvents.FILE_SELECTED, self.update_data_list)
        EventManager.subscribe(BuiltInEvents.FILE_UNLOADED, self.clear)
        
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.installEventFilter(RightClickedFilter(self))

        self.treemap     = {}
        self.openParsers = {}
    
    def getItemOffsetFromHeader(self, qPoint):
        """Calculate the offset of the item from the header."""
        header = self.header()
        if not header:
            return qPoint
        return qPoint - QPoint(0,header.geometry().height())

    def clear(self,filename:str=None):
        if(filename):
            LOG.info(f"Clearing data list for file: {filename}")
            if filename in self.treemap:
                item = self.treemap.pop(filename)
                self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        else:
            LOG.info("Clearing entire data list")
            self.treemap.clear()
            super().clear()

    def on_item_right_clicked(self, item, column):
        
        """Handle right-click events on items."""
        LOG.info(f"Item right-clicked: {item.text(0)}")
        menu = QMenu(self)
        action = menu.addAction("Remove Item")
        action.triggered.connect(lambda: self.clear(item.text(0)))
        menu.exec(self.viewport().mapToGlobal(item.pos()))

    def update_data_list(self, filename):
        if filename in self.openParsers:
            LOG.info(f"Data list already updated for file: {filename}")
            return
        LOG.info(f"Updating data list with file: {filename}")
        ext = os.path.splitext(filename)[-1]
        # path,name = os.path.split(filename)
        # name = os.path.join(os.path.split(path)[-1], name)
        if ext in ACTIVE_PARSERS:
            data = ACTIVE_PARSERS[ext](filename)
            self.openParsers[filename] = data
            parent = QTreeWidgetItem(self,[filename, ext])
            self.addTopLevelItem(parent)
            self.treemap[filename] = parent
            for item in data:
                tree_item = QTreeWidgetItem(parent)
                tree_item.setText(0, item)
        else:
            LOG.warning(f"No parser found for file extension: {ext}")
    
    def on_item_double_clicked(self, item, column):
        """Handle double-click events on items."""
        key = item.text(0)
        LOG.info(f"Item double-clicked: {key}")
        
        if item.parent() is not None:
            filename = item.parent().text(0)
            if filename in self.openParsers:
                parser = self.openParsers[filename]
                # Here you can add logic to display the data or perform actions with the parser
                LOG.info(f"Parser for {filename} is {parser.name()}")
                EventManager.trigger(
                    BuiltInEvents.DATA_SElECTED,
                    data=parser.data(key),
                    filename=filename,
                )
            else:
                LOG.warning(f"No parser found for item: {filename}")