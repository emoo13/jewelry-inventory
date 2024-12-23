from PyQt5 import QtCore, QtGui, QtWidgets

class InventoryUi(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(InventoryUi, self).__init__(parent)
        self.category_tool_tip = "Category of jewelry to choose from"
        self.name_tool_tip = "Name of jewelry to choose from"

        self.setWindowTitle("Elladay Inventory Manager")
        self.setFixedWidth(1781)
        self.setFixedHeight(1194)
        self.setup_ui()

    def setup_ui(self):
        window_vertical_layout = QtWidgets.QVBoxLayout(self)

        main_hor_layout = QtWidgets.QHBoxLayout(self)
        main_hor_layout.setContentsMargins(0, 0, 0, 0)
        main_hor_layout.setObjectName("main_hor_layout")

        self.setup_title(window_vertical_layout)
        self.setup_search(window_vertical_layout)
        self.setup_main_group(main_hor_layout)
        window_vertical_layout.addLayout(main_hor_layout)

    def setup_title(self, parent_layout):
        welcome_label = QtWidgets.QLabel("Welcome to the Elladay Soptera Inventory Manager!")
        welcome_label.setGeometry(QtCore.QRect(470, 10, 911, 82))

        font = QtGui.QFont()
        font.setFamily("Californian FB")
        font.setPointSize(36)
        font.setItalic(True)
        welcome_label.setFont(font)
        welcome_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        parent_layout.addWidget(welcome_label)

    def setup_body(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        vertical_layout = QtWidgets.QVBoxLayout()

    def setup_search(self, parent_layout):
        main_group_box = QtWidgets.QGroupBox()

        search_hor_layout = QtWidgets.QHBoxLayout(main_group_box)
        search_hor_layout.setContentsMargins(0, 0, 0, 0)
        search_bar = QtWidgets.QLineEdit()
        font = QtGui.QFont()
        font.setPointSize(18)
        search_bar.setFont(font)
        search_bar.setPlaceholderText("🔍 Search Jewelry")

        search_hor_layout.addWidget(search_bar)
        parent_layout.addWidget(main_group_box)

    def setup_main_group(self, parent_layout):
        jewel_group_box = QtWidgets.QGroupBox()
        jewel_hor_layout = QtWidgets.QHBoxLayout(jewel_group_box)
        jewel_hor_layout.setGeometry(QtCore.QRect(20, 20, 1731, 931))

        jewel_table = QtWidgets.QTableWidget()
        jewel_table.setMaximumSize(QtCore.QSize(34260, 900))
        jewel_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        jewel_table.setColumnCount(9)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(8)
        item.setFont(font)
        item.setText("Select")

        jewel_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Image")
    
        jewel_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Name")

        jewel_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Quantity")

        jewel_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Manufacturer")

        jewel_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("SKU")

        jewel_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Platform")

        jewel_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Created Date")

        jewel_table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Sell Price")

        jewel_table.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()

        tabWidget, details = self.setup_tabs()
        self.details_tab(details)

        jewel_hor_layout.addWidget(jewel_table)
        jewel_hor_layout.addWidget(tabWidget)
        parent_layout.addWidget(jewel_group_box)

    def setup_tabs(self):
        # Details tab
        detail_hor_layout = QtWidgets.QWidget()
        details_tab = QtWidgets.QWidget()
        details_group_box = QtWidgets.QGroupBox(details_tab)
        details_group_box.setGeometry(QtCore.QRect(10, 10, 581, 871))
        details_group_box.setTitle("Details")

        # Dimensions tab
        dims_tab = QtWidgets.QWidget()
        dims_group_box = QtWidgets.QGroupBox(dims_tab)
        dims_group_box.setGeometry(QtCore.QRect(10, 10, 581, 871))

        # Pricing Tab
        price_tab = QtWidgets.QWidget()
        price_group_box = QtWidgets.QGroupBox(price_tab)
        price_group_box.setGeometry(QtCore.QRect(10, 10, 581, 871))

        # Status Tab
        status_tab = QtWidgets.QWidget()
        status_group_box = QtWidgets.QGroupBox(status_tab)
        status_group_box.setGeometry(QtCore.QRect(10, 10, 581, 871))

        tabWidget = QtWidgets.QTabWidget()
        tabWidget.setMaximumSize(QtCore.QSize(617, 16777215))

        font = QtGui.QFont()
        font.setPointSize(11)
        tabWidget.setFont(font)
        tabWidget.setIconSize(QtCore.QSize(16, 16))

        tabWidget.addTab(details_tab,"")
        tabWidget.setTabText(0, "Stock Details")

        tabWidget.addTab(dims_tab,"")
        tabWidget.setTabText(1, "Dimensions")

        tabWidget.addTab(price_tab,"")
        tabWidget.setTabText(2, "Pricing Info")

        tabWidget.addTab(status_tab,"")
        tabWidget.setTabText(3, "Status")
        product_details_label = QtWidgets.QLabel()

        return tabWidget, details_group_box
    
    def details_tab(self, details_group_box):
        layoutWidget_15 = QtWidgets.QWidget(details_group_box)
        layoutWidget_15.setGeometry(QtCore.QRect(40, 130, 331, 32))
        category_hor_layout = QtWidgets.QHBoxLayout()
        category_hor_layout.setContentsMargins(0, 0, 0, 0)
        category_label = QtWidgets.QLabel()
        category_label.setMaximumSize(QtCore.QSize(115, 30))

        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        category_label.setFont(font)
        category_label.setText("Category:")

        category_hor_layout.addWidget(category_label)
        category_pt_edit = QtWidgets.QPlainTextEdit()
        category_pt_edit.setMaximumSize(QtCore.QSize(150, 30))
        category_pt_edit.setBackgroundVisible(False)
        category_hor_layout.addWidget(category_pt_edit)
