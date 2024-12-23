import view
from PyQt5 import QtWidgets
import sys

import view.inventory_view
import view.ui

class App(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        # self.model = view.ui.AnimaticModel()
        # self.main_controller = view.ui.AnimaticMainController(self.model)
        self.main_view = view.ui.InventoryUi()
        # self.main_view = view.ui.InventoryUi()
        self.main_view.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
    # dict_var = {
    #     "var1": "dog",
    #     "var2": "cat",
    #     "var3": "bird",
    #     "var4": "fish"
    # }