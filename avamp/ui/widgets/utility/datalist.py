from avamp.core.logging import LOG
from avamp.core.parsers.base_parser import BaseParser, InterfaceGroup
from avamp.core.parsers import PARSERS,ACTIVE_PARSERS
from avamp.core.event_manager import EventManager, BuiltInEvents

from PySide6.QtWidgets import QWidget, QGridLayout, QMenuBar, QTreeWidget, QTreeWidgetItem, QMenu
from PySide6.QtCore import QObject, QEvent, QEventLoop, QPoint

import os

#Custom tree item that can store additional data
class DataTreeItem(QTreeWidgetItem):
    def __init__(self, parent, key,interface,filename):
        super().__init__(parent)
        self.key = key
        self.interface = interface
        self.filename = filename

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
        self.setColumnWidth(0, 200)
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

    def update_data_list_children(self, data: InterfaceGroup, parent: QTreeWidgetItem, filename:str):
        for key, value in data: 
            if isinstance(value, InterfaceGroup):
                LOG.debug(f"Adding child item to data list: {key}")
                tree_item = QTreeWidgetItem(parent)
                tree_item.setText(0, key)
                self.update_data_list_children(value, tree_item,filename)
            else:
                LOG.debug(f"Adding child item to data list: {key}")
                tree_item = DataTreeItem(parent, key, value,filename)
                tree_item.setText(0, key)
                tree_item.setText(1, value.type())

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
            for key,value in data:
                if(isinstance(value, InterfaceGroup)):
                    LOG.debug(f"Adding interface group to data list: {key}")
                    tree_item = QTreeWidgetItem(parent)
                    tree_item.setText(0, key)
                    self.update_data_list_children(value, tree_item,filename)
                else:
                    LOG.debug(f"Adding item to data list: {key}")
                    tree_item = DataTreeItem(parent,key,value,filename)
                    tree_item.setText(0, key)
                    tree_item.setText(1, value.type())
        else:
            LOG.warning(f"No parser found for file extension: {ext}")
    
    def on_item_double_clicked(self, item, column):
        """Handle double-click events on items."""
        key = item.text(0)
        LOG.info(f"Item double-clicked: {key}")
        if len(self.selectedItems()) > 1:
            self.trigger_collected_visual(self.selectedItems())
        else:
            self.trigger_visual(item)
        
    def trigger_collected_visual(self, items):
        data = []
        for item in items:
            if item.parent() is not None:
                # filename = item.parent().text(0)
                # if filename in self.openParsers:
                    # parser = self.openParsers[filename]
                data.append(item.interface)
                LOG.info(f"Selected data: {item.text(0)} from file: {item.filename}")
                # else:
                    # LOG.warning(f"No parser found for item: {filename}")
        if not data: 
            LOG.warning("No data selected for combined visual")
            return
        collected_data = data[0].combine(data[1:])
        LOG.info(f"Combined data: {collected_data.name()} from file: {item.filename}")
        EventManager.trigger(
            BuiltInEvents.DATA_SElECTED,
            data=collected_data,
            filename=item.filename,
        )   

    def trigger_visual(self, item):
        key = item.text(0)
        if item.parent() is not None:
            # filename = item.parent().text(0)
            # if filename in self.openParsers:
                # parser = self.openParsers[filename]
                # Here you can add logic to display the data or perform actions with the parser
            LOG.info(f"Parser for {item.filename}, key: {key} selected")
            EventManager.trigger(
                BuiltInEvents.DATA_SElECTED,
                data=item.interface,
                filename=item.filename,
            )
