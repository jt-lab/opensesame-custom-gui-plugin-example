"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.canvas import Canvas
from qtpy import QtGui, QtCore, QtWidgets


class ListWithAdd(QtWidgets.QWidget):
    """ This is an example for a simple custom widget. For most real
    applications it would probably make sense to put such classes in
    external files and load the GUI from a .ui-file. But let's keep
    everythig together here for simplicity 
    """
    textChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.list = QtWidgets.QListWidget()
        self.add_btn = QtWidgets.QPushButton("+")
        self.add_btn.setFixedWidth(30)

        # Horizontal layout: list + button
        h = QtWidgets.QHBoxLayout()
        h.addWidget(self.list)
        h.addWidget(self.add_btn)

        # Main layout
        v = QtWidgets.QVBoxLayout(self)
        v.addLayout(h)

        # Connect button
        self.add_btn.clicked.connect(self.add_item)        
        self.list.itemChanged.connect(self.on_item_changed)        

    def on_item_changed(self):
        self.textChanged.emit(self.text())
    
    def text(self):
        """ We need this for serialization (for script view and saving) """
        return ",".join(self.list.item(i).text() for i in range(self.list.count()))

    def setText(self, text):
        self.list.clear()
        if text:
            for item in text.split(","):
                self.list.addItem(item)
        self.textChanged.emit(self.text())
          
    def add_item(self):
        text, ok = QtWidgets.QInputDialog.getText(
            self, "Add Item", "Enter text:")
        if ok and text:
            self.list.addItem(text)

class ExampleCustomPlugin(Item):
    def reset(self):
        """Resets plug-in to initial values."""
        self.var.checkbox = 'yes'
        #self.var.custom_list = ''

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        super().prepare()
        self.c = Canvas(self.experiment)
        self.c.fixdot()

    def run(self):
        """The run phase of the plug-in goes here."""
        self.set_item_onset(self.c.show())

class QtExampleCustomPlugin(ExampleCustomPlugin, QtAutoPlugin):
    def __init__(self, name, experiment, script=None):
        ExampleCustomPlugin.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):

        super().init_edit_widget()
        
        # Create out custom widget
        cl = ListWithAdd()
        
        # Add it into the desired position among the auto-generated
        # widgets. Note there might be a stretch at the end
        index = self.edit_vbox.count() - 2
        self.edit_vbox.insertWidget(index, cl)

        # Let's have it managed like a line edit. This means the ListWithAdd
        # must quack like a line edit, emitting the right signals, etc.
        self.auto_line_edit['custom_list'] = cl
