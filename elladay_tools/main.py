from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
# from PyQt5.QtCore import Qt, QRect
# from PyQt5.QtGui import QPainter
# from PyQt5.QtWidgets import QStyledItemDelegate
import model
import controller
import sys
import qdarkstyle
import qdarkgraystyle
import os
from datetime import datetime

MIN_COLUMN_WIDTH = 20
PRODUCT_ID_MONGO = '67686573e3da599d42c6db51'
GEMSTONE_ID_MONGO = '676853d7e3da599d42c6db50'
METADATA_ID_MONGO = '6767ba05bcb627079b8d3806'

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        self.model_obj = model.MongoModel()
        self.controller_obj = controller.MongoController()
        self.shade_list = []
        self.hex_list = []
        self.large_shade_list = []
        self.large_gemtype_list = []
        self.model_connection = self.model_obj.connection_to_mongo()
        self.color_list = self.color_query()
        self.cond_list = self.condition_query()
        self.cat_list = self.category_query()
        self.subcat_list = self.subcategory_query()
        self.plat_list = self.platforms_query()
        self.sell_status_list = self.sell_status_query()
        self.product_list = self.product_query()
        table_data = self.controller_obj.process_products(self.product_list)
        self.sub_gem_result = []
        self.window = loadUi("final_inventory_final.ui", self)
        self.new_gemstone_button = self.window.new_gemstone_button
        self.new_gemstone_button.clicked.connect(lambda: self.open_gem_secondary_ui("gemstone_manage.ui"))

        self.label_location_pt_edit = self.window.label_location_pt_edit
        self.label_location_pt_edit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.search_label_dir_button = self.window.search_label_dir_button
        self.search_label_dir_button.clicked.connect(lambda: self.open_file_label_dialog(self.label_location_pt_edit))

        self.excel_location_pt_edit = self.window.excel_location_pt_edit
        self.excel_location_pt_edit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.search_excel_dir_button = self.window.search_excel_dir_button
        self.search_excel_dir_button.clicked.connect(lambda: self.open_file_label_dialog(self.excel_location_pt_edit))
        self.excel_button = self.window.excel_button
        self.excel_button.clicked.connect(self.export_to_excel)

        self.manage_category_button = self.window.manage_category_button
        self.manage_category_button.clicked.connect(lambda: self.open_secondary_ui("new_category.ui"))
        
        self.manage_metal_button = self.window.manage_metal_button
        self.manage_metal_button.clicked.connect(lambda: self.open_secondary_ui("new_metal.ui"))

        self.search_bar = self.window.search_bar
        self.search_bar.installEventFilter(self)
        self.search_button = self.window.search_button
        self.search_button.clicked.connect(self.on_search_pressed)
        self.clear_search_button = self.window.clear_search_button
        self.clear_search_button.clicked.connect(self.on_clear_search_pressed)
        self.clear_search_button.clicked.connect(self.on_clear_search_pressed)
        self.delete_button = self.window.delete_button
        self.delete_button.clicked.connect(self.on_delete_from_table)

        # Detail Tab
        self.all_clear_button.clicked.connect(self.clear_all)
        self.all_save_button.clicked.connect(self.on_tab_save)

        self.calendar = QtWidgets.QCalendarWidget(self)
        self.calendar.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.SingleLetterDayNames)
        self.calendar.clicked[QtCore.QDate].connect(self.on_date_selected)

        self.images_directory_pt_edit = self.window.images_directory_pt_edit
        self.image_label1 = self.window.image_label1
        self.image_label2 = self.window.image_label2
        self.image_label3 = self.window.image_label3
        self.image_label4 = self.window.image_label4
        self.image_label5 = self.window.image_label5
        self.image_label6 = self.window.image_label6
        self.platform_combo_box = self.window.platform_combo_box
        self.platform_combo_box.addItems(self.plat_list)
        self.sell_status_combo_box = self.window.sell_status_combo_box
        self.sell_status_combo_box.addItems(self.sell_status_list)
        self.research_pt_edit = self.window.research_pt_edit
        self.url_pt_edit = self.window.url_pt_edit
        self.my_price_pt_edit = self.window.my_price_pt_edit
        self.misc_description_box = self.window.misc_description_box
        self.tag_list_widget = self.window.tag_list_widget
        self.created_result_label = self.window.created_result_label
        self.weight_before_pt_edit = self.window.weight_before_pt_edit
        self.weight_after_pt_edit = self.window.weight_after_pt_edit
        self.sub_category_combo_box = self.window.sub_category_combo_box
        self.updated_result_label = self.window.updated_result_label
        self.tag_pt_edit = self.window.tag_pt_edit
        self.tag_pt_edit.installEventFilter(self)
        self.tag_pt_edit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.print_stat_result_label = self.window.print_stat_result_label
        self.print_button = self.window.print_button
        self.print_button.clicked.connect(self.print_data_label)

        self.posted_pt_edit = self.window.posted_pt_edit
        self.posted_pt_edit.mousePressEvent = self.show_calendar

        # Dimensions
        self.len_pt_edit = self.window.len_pt_edit
        self.width_pt_edit = self.window.width_pt_edit
        self.height_pt_edit = self.window.height_pt_edit

        self.clasp_len_pt_edit = self.window.clasp_len_pt_edit
        self.clasp_width_pt_edit = self.window.clasp_width_pt_edit
        self.clasp_height_pt_edit = self.window.clasp_height_pt_edit

        self.focal_len_pt_edit = self.window.focal_len_pt_edit
        self.focal_width_pt_edit = self.window.focal_width_pt_edit
        self.focal_height_pt_edit = self.window.focal_height_pt_edit

        self.pin_len_pt_edit = self.window.pin_len_pt_edit
        self.pin_width_pt_edit = self.window.pin_width_pt_edit

        self.dimension_pt_list = [self.len_pt_edit,
                            self.width_pt_edit,
                            self.height_pt_edit,
                            self.clasp_len_pt_edit,
                            self.clasp_width_pt_edit,
                            self.clasp_height_pt_edit,
                            self.focal_len_pt_edit,
                            self.focal_width_pt_edit,
                            self.focal_height_pt_edit,
                            self.pin_len_pt_edit,
                            self.pin_width_pt_edit]

        self.dim_clear_button = self.window.dim_clear_button
        self.dim_clear_button.clicked.connect(lambda: self.clear_tab(pt_list=self.dimension_pt_list))

        # Pricing
        self.price_pt_list = [
            self.research_pt_edit,
            self.my_price_pt_edit,
            self.url_pt_edit
        ]
        self.price_combo_list = [
            self.sell_status_combo_box,
            self.platform_combo_box]
        self.price_clear_button = self.window.price_clear_button
        self.price_clear_button.clicked.connect(lambda: self.clear_tab(pt_list=self.price_pt_list, combo_list=self.price_combo_list))

        # Status
        self.photo_checkbox = self.window.photo_checkbox
        self.measure_checkbox = self.window.measure_checkbox
        self.cleaning_checkbox = self.window.cleaning_checkbox
        self.repair_checkbox = self.window.repair_checkbox
        self.weighing_checkbox = self.window.weighing_checkbox
        self.listed_checkbox = self.window.listed_checkbox
        self.boxing_checkbox = self.window.boxing_checkbox
        self.checkboxes = [self.photo_checkbox, self.measure_checkbox, self.cleaning_checkbox, self.repair_checkbox,
                           self.weighing_checkbox, self.listed_checkbox, self.boxing_checkbox]
        self.status_clear_button = self.window.status_clear_button
        self.status_clear_button.clicked.connect(lambda: self.clear_tab(check_list=self.checkboxes))

        #   - Gems Comboboxes
        self.gem_list = self.gem_query()
        self.gem_names = self.controller_obj.process_materials(self.gem_list)
        self.clarity_list = self.clarity_query()
        self.cut_list = self.cut_query()
        self.gemstone_combo_box = self.window.gemstone_combo_box
        self.gemstone_combo_box.addItems(self.gem_names)
        self.gemstone_combo_box.setCurrentIndex(-1)
        self.gemstone_combo_box.activated.connect(self.show_dropdown)
        self.gemstone_combo_box.currentIndexChanged.connect(self.populate_subgem_dropdown)
        self.type_combo_box = self.window.type_combo_box

        self.clarity_combo_box = self.window.clarity_combo_box
        self.clarity_combo_box.addItems(self.clarity_list)
        self.clarity_combo_box.setCurrentIndex(-1)

        self.cut_combo_box = self.window.cut_combo_box
        self.cut_combo_box.addItems(self.cut_list)
        self.gemstone_combo_box.setCurrentIndex(-1)

        self.carat_gem_pt_edit = self.window.carat_gem_pt_edit

        #   - Metal Comboboxes
        metal_list = self.metal_query()
        self.metal_names = self.controller_obj.process_materials(metal_list)
        self.plating_list = self.plating_query()
        self.metal_combo_box = self.window.metal_combo_box
        self.metal_combo_box.addItems(self.metal_names)
        self.carat_pt_edit = self.window.carat_pt_edit
        self.plated_combo_box = self.window.plated_combo_box
        self.plated_combo_box.addItems(self.plating_list)

        #   - Conditions ComboBox
        self.condition_combo_box = self.window.condition_combo_box
        self.condition_combo_box.addItems(self.cond_list)
        self.condition_combo_box.setCurrentIndex(-1)
        self.condition_combo_box.activated.connect(self.show_dropdown)

        #   - Handmade ComboBox
        self.handmade_combo_box = self.window.handmade_combo_box

        self.handmade_list = ["", "Yes", "No", "Unknown"]
        self.handmade_combo_box.addItems(self.handmade_list)
        self.handmade_combo_box.setCurrentIndex(-1)
        self.handmade_combo_box.activated.connect(self.show_dropdown)

        #   - Colors ComboBox
        self.color_combo_box = self.window.color_combo_box
        self.color_combo_box.addItems(self.color_list)
        self.color_combo_box.setCurrentIndex(-1)
        self.color_combo_box.activated.connect(self.show_dropdown)
        self.color_combo_box.currentIndexChanged.connect(self.populate_shade_dropdown)

        self.shade_combo_box = self.window.shade_combo_box
        self.shade_combo_box.setCurrentIndex(-1)
        self.shade_combo_box.currentIndexChanged.connect(self.shade_dropdown)
        
        #   - Category ComboBox
        self.category_combo_box = self.window.category_combo_box
        # self.category_combo_box.setEditable(True)
        self.category_combo_box.addItems(self.cat_list)
        self.category_combo_box.setCurrentIndex(-1)
        self.category_combo_box.activated.connect(self.show_dropdown)
        self.sub_category_combo_box.addItems(self.subcat_list)
        self.sub_category_combo_box.setCurrentIndex(-1)
        self.sub_category_combo_box.activated.connect(self.show_dropdown)
        
        #   - Manufacturer LineEdit
        self.manuf_pt_edit = self.window.manuf_pt_edit

        self.color_display = self.window.color_display

        # Details Variables
        self.quan_pt_edit = self.window.quan_pt_edit
        self.sku_pt_edit = self.window.sku_pt_edit
        self.tag_list_widget = self.window.tag_list_widget
        self.name_pt_edit = self.window.name_pt_edit
        self.tag_pt_edit = self.window.tag_pt_edit
        self.created_result_label = self.window.created_result_label
        self.updated_result_label = self.window.updated_result_label
        self.print_stat_result_label = self.window.print_stat_result_label

        self.detail_pt_list = [
            self.name_pt_edit,
            self.manuf_pt_edit,
            self.quan_pt_edit,
            self.sku_pt_edit,
            self.tag_pt_edit,
            self.carat_pt_edit,
            self.carat_gem_pt_edit,
            self.tag_list_widget
        ]
        self.detail_combo_list = [
            self.condition_combo_box,
            self.handmade_combo_box,
            self.color_combo_box,
            self.shade_combo_box,
            self.category_combo_box,
            self.metal_combo_box,
            self.plated_combo_box,
            self.gemstone_combo_box,
            self.type_combo_box,
            self.clarity_combo_box,
            self.cut_combo_box
        ]
        self.detail_gp_list = [
            self.color_display
        ]
        self.detail_clear_button = self.window.detail_clear_button
        self.detail_clear_button.clicked.connect(lambda: self.clear_tab(pt_list=self.detail_pt_list,
                                                                       combo_list=self.detail_combo_list,
                                                                       gp_list=self.detail_gp_list))

        # Table Formatting
        self.jewel_table = self.window.jewel_table
        self.populate_table(table_data)
        font = self.jewel_table.font()
        font.setPointSize(12)
        self.jewel_table.setFont(font)
        header = self.jewel_table.horizontalHeader()
        self.jewel_table.itemSelectionChanged.connect(self.row_selected)
        # Stretch all other columns
        for col in range(1, self.jewel_table.columnCount()):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Interactive)

        self.jewel_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.jewel_table.itemSelectionChanged.connect(self.highlight_row)

        self.upload_button = self.window.upload_button
        self.upload_button.clicked.connect(self.open_file_dialog)

        # Misc
        self.misc_clear_button = self.window.misc_clear_button
        self.misc_clear_button.clicked.connect(lambda: self.clear_tab(pt_list=[self.misc_description_box]))
        self.installEventFilter(self)

    # def name_gem_delete(self, combobox, name_text):
    #     self.model_obj.delete_gemstones_from_db("name",
    #                                             name_text,
    #                                             parent_key="gemstones")
    #     self.gem_list = self.gem_query()
    #     self.gem_names = self.controller_obj.process_materials(self.gem_list)
    #     combobox.clear()
    #     combobox.addItems(self.gem_names)

    # def clarity_gem_delete(self, combobox):
    #     self.model_obj.delete_gemstones_from_db("acronym",
    #                                             combobox.currentText().upper(),
    #                                             parent_key="gemstone_clarity_types")
    #     self.clarity_list = self.clarity_query()
    #     combobox.clear()
    #     combobox.addItems(self.clarity_list)

    # def cut_gem_delete(self, combobox):
    #     self.model_obj.delete_gemstones_from_db("name",
    #                                             combobox.currentText().lower(),
    #                                             parent_key="gemstone_cuts")
    #     self.cut_list = self.cut_query()
    #     combobox.clear()
    #     combobox.addItems(self.cut_list)

    def delete_sub_data(self, key, combobox, name_text, parent_key=None, types=False):
        name_items = [x.lower() for x in self.get_combobox_items(combobox)]
        if types:
            self.model_obj.delete_gemstones_from_db("types",
                                                    name_text,
                                                    types=True)
        else:
            self.model_obj.delete_gemstones_from_db(key,
                                                    name_text,
                                                    parent_key=parent_key)
        name_items.remove(name_text.lower())
        name_items = [word.capitalize() for word in name_items]
        combobox.clear()
        combobox.addItems(sorted(name_items))
        combobox.setCurrentIndex(-1)

    def open_gem_secondary_ui(self, ui_name):
        # Create a new instance of the second UI (gem.ui)
        self.second_ui = QtWidgets.QDialog()  # You can use a QWidget or QDialog
        loadUi(ui_name, self.second_ui)  # Load gem.ui into the second_ui window

        # Populate comboboxes
        name_combo_box = self.second_ui.findChild(QtWidgets.QComboBox, "name_combo_box")
        name_combo_box.addItems(self.gem_names)

        type_combo_box = self.second_ui.findChild(QtWidgets.QComboBox, "type_combo_box")
        subgem_list = ['']
        for gem in self.gem_list:
            subgem_results = self.controller_obj.process_subgemstones(self.gem_list, gem["name"])
            subgem_list = subgem_list + subgem_results
        type_combo_box.addItems(sorted(subgem_list))
        type_combo_box.setCurrentIndex(-1)

        clarity_combo_box = self.second_ui.findChild(QtWidgets.QComboBox, "clarity_combo_box")
        clarity_combo_box.addItems(self.clarity_list)

        cut_combo_box = self.second_ui.findChild(QtWidgets.QComboBox, "cut_combo_box")
        cut_combo_box.addItems(self.cut_list)

        # ---- Deleting ----
        name_delete_button = self.second_ui.findChild(QtWidgets.QPushButton, "name_delete_button")
        type_delete_button = self.second_ui.findChild(QtWidgets.QPushButton, "type_delete_button")
        clarity_delete_button = self.second_ui.findChild(QtWidgets.QPushButton, "clarity_delete_button")
        cut_delete_button = self.second_ui.findChild(QtWidgets.QPushButton, "cut_delete_button")

        name_delete_button.clicked.connect(lambda: self.delete_sub_data("name",
                                                                        name_combo_box,
                                                                        name_combo_box.currentText().lower(),
                                                                        parent_key="gemstones"))
        type_delete_button.clicked.connect(lambda: self.delete_sub_data("types",
                                                                        type_combo_box,
                                                                        type_combo_box.currentText().lower(),
                                                                        types=True))
        clarity_delete_button.clicked.connect(lambda: self.delete_sub_data("acronym",
                                                                        clarity_combo_box,
                                                                        clarity_combo_box.currentText().upper(),
                                                                        parent_key="gemstone_clarity_types"))
        cut_delete_button.clicked.connect(lambda: self.delete_sub_data("name",
                                                                        cut_combo_box,
                                                                        cut_combo_box.currentText().lower(),
                                                                        parent_key="gemstone_cuts"))

        # ---- Adding ----
        add_button = self.second_ui.findChild(QtWidgets.QPushButton, "add_button")
        cancel_button = self.second_ui.findChild(QtWidgets.QPushButton, "cancel_button")

        name_pt_edit = self.second_ui.findChild(QtWidgets.QPlainTextEdit, "name_pt_edit")
        type_pt_edit = self.second_ui.findChild(QtWidgets.QPlainTextEdit, "type_pt_edit")
        clarity_pt_edit = self.second_ui.findChild(QtWidgets.QPlainTextEdit, "clarity_pt_edit")
        cut_pt_edit = self.second_ui.findChild(QtWidgets.QPlainTextEdit, "cut_pt_edit")
        gemstone_name_label = self.second_ui.findChild(QtWidgets.QLabel, "gemstone_name_label")
        gemstone_type_label = self.second_ui.findChild(QtWidgets.QLabel, "gemstone_type_label")
        gemstone_clarity_label = self.second_ui.findChild(QtWidgets.QLabel, "gemstone_clarity_label")
        gemstone_cut_label = self.second_ui.findChild(QtWidgets.QLabel, "gemstone_cut_label")

        gem_labels = ["name", "types", "gemstone_clarity_types", "gemstone_cuts"]
        

        line_list = [name_pt_edit, type_pt_edit, clarity_pt_edit, cut_pt_edit]
        add_button.clicked.connect(lambda: self.get_pt_items(gem_labels, line_list))

        # Show the second UI
        self.second_ui.show()

    def get_pt_items(self, label_list, pt_list):
        dict_data = {}
        for i, val in enumerate(pt_list):
            if i == 1:
                type_field = val.toPlainText()
                if type_field:
                    type_split = val.toPlainText().split(",")
                    trimmed_strings = [s.lstrip() for s in type_split]
                else:
                    trimmed_strings = []
                dict_data[label_list[i]] = trimmed_strings
            else:
                dict_data[label_list[i]] = val.toPlainText()
        
        new_gemstone = {
            "gemstones": [
                {
                    "name": dict_data["name"],
                    "types": dict_data["types"]
                    }
                ]
            }
        
        self.model_obj.create_new_entry(new_gemstone, "gemstones", GEMSTONE_ID_MONGO)
        return dict_data

    def get_combobox_items(self, combobox):
        combo_box_items = []
        for index in range(combobox.count()):
            combo_box_items.append(combobox.itemText(index))
        return combo_box_items

    def export_to_excel(self):
        excel_location = self.excel_location_pt_edit.toPlainText()
        self.model_obj.export_to_excel(excel_location)

    def clear_all(self):
        """ Clear every single field in the tab widget """
        misc_pt_list = [self.posted_pt_edit, self.created_result_label,
                        self.updated_result_label, self.print_stat_result_label, self.misc_description_box,
                        self.images_directory_pt_edit, self.image_label1, self.image_label2, self.image_label3,
                        self.image_label4, self.image_label5, self.image_label6, self.tag_list_widget]
        list_of_pts = [self.dimension_pt_list, self.price_pt_list, self.detail_pt_list, misc_pt_list]
        for pt_list in list_of_pts:
            for obj in pt_list:
                obj.clear()
        self.clear_tab(check_list=self.checkboxes, combo_list=self.detail_combo_list, gp_list=self.detail_gp_list)

    def clear_tab(self, pt_list=None, combo_list=None, check_list=None, gp_list = None):
        """ Clear every single field in the specified tab """
        if pt_list:
            for obj in pt_list:
                obj.clear()
        if combo_list:
            for obj in combo_list:
                obj.setCurrentIndex(0)
        if check_list:
            for obj in check_list:
                obj.setChecked(False)
        if gp_list:
            for obj in gp_list:
                obj.setStyleSheet("QGroupBox { background-color: transparent; }")

    def on_clear_search_pressed(self):
        self.search_bar.clear()
        table_data = self.controller_obj.process_products(self.product_list)
        self.populate_table(table_data)

    def on_tag_pressed(self):
        contained_text = self.tag_pt_edit.toPlainText()
        tag_list_contents = self.get_list_widget_items()
        if contained_text:
            tag_list = contained_text.split(',')
            trimmed_strings = [s.lstrip() for s in tag_list]
            new_list = [item for item in trimmed_strings if item not in tag_list_contents]
            lower_list = [x.lower() for x in new_list]
            self.tag_list_widget.addItems(lower_list)
    
    def on_delete_from_table(self):
        selected_items = self.jewel_table.selectedItems()
        selected_rows_data = []

        # Loop through all selected items
        for item in selected_items:
            row = item.row()  # Get the row number for the current item
            
            # If the row is not already added to the selected_rows_data, create a new list for this row
            if len(selected_rows_data) <= row:
                selected_rows_data.append([item.text()])
            else:
                selected_rows_data[row].append(item.text())

        # Filter out rows that were not selected or have no data
        selected_rows_data = [row_data for row_data in selected_rows_data if row_data]
        # selected_row_data = [item.text() for item in selected_items if item.row() == selected_items[0].row()]
        for product in selected_rows_data:
            if not product == ['']:
                prod_id = product[9]
                self.model_obj.delete_from_db(prod_id)
                self.product_list = self.product_query()
                table_data = self.controller_obj.process_products(self.product_list)
                self.populate_table(table_data)

    def on_search_pressed(self):
        contained_text = self.search_bar.text()
        searched_results = self.controller_obj.process_search(contained_text, self.product_list)
        if searched_results:
            table_data = self.controller_obj.process_products(searched_results)
            self.populate_table(table_data)
        else:
            self.jewel_table.clear()

    def eventFilter(self, source, event):
        if source == self.tag_pt_edit and event.type() == event.KeyPress:
            if event.key() == QtCore.Qt.Key_Return:
                self.on_tag_pressed()
                self.tag_pt_edit.clear()
                return True
        if source == self.search_bar and event.type() == event.KeyPress:
            if event.key() == QtCore.Qt.Key_Return:
                self.on_search_pressed()
        if source != self.calendar and event.type() == QtCore.QEvent.MouseButtonPress:
            # Close the calendar when a click happens outside it
            self.calendar.setVisible(False)

        return super().eventFilter(source, event)

    def row_selected(self):
        """ Display product data on the tab widget from the table selection """
        # Get selected items
        selected_items = self.jewel_table.selectedItems()
        self.tag_pt_edit.clear()
        self.tag_list_widget.clear()

        if selected_items:
            # Group by rows
            selected_row_data = [item.text() for item in selected_items if item.row() == selected_items[0].row()]
            item_id = selected_row_data[4]
            array_data = self.model_obj.sku_query(item_id)

            # ----- Details -----
            self.quan_pt_edit.setPlainText(str(array_data["quantity_in_stock"]))
            self.sku_pt_edit.setPlainText(array_data["sku"])
            self.name_pt_edit.setPlainText(array_data["product_name"])
            self.posted_pt_edit.setPlainText(array_data["date_posted"])
            self.carat_gem_pt_edit.setPlainText(str(array_data["gemstone_details"]["carat_weight"]))
            self.manuf_pt_edit.setPlainText(array_data["brand"])
            self.weight_after_pt_edit.setPlainText(array_data["weight_after"])
            self.weight_before_pt_edit.setPlainText(array_data["weight_before"])

            if array_data["label_printed"] == "No":
                self.print_stat_result_label.setText("<font color='red'>" + array_data["label_printed"] + "</font>")
            else:
                self.print_stat_result_label.setText("<font color='green'>" + array_data["label_printed"] + "</font>")

            list_widget_items = self.get_list_widget_items()
            new_list = [item for item in array_data["tags"] if item not in list_widget_items]
            self.tag_list_widget.addItems(new_list)
            
            index = self.set_by_index_dict(self.gem_list, array_data["gemstone"], 'name')
            self.gemstone_combo_box.setCurrentIndex(index)
            
            index = self.set_by_index_list(self.subcat_list, array_data["subcategory"])
            self.sub_category_combo_box.setCurrentIndex(index)

            index = self.set_by_index_list(self.clarity_list, array_data["gemstone_details"]["clarity"])
            self.clarity_combo_box.setCurrentIndex(index)

            index = self.set_by_index_list(self.cut_list, array_data["gemstone_details"]["cut"])
            self.cut_combo_box.setCurrentIndex(index)

            index = self.set_by_index_list(self.metal_names, array_data["metal_type"])
            self.metal_combo_box.setCurrentIndex(index)

            index = self.set_by_index_list(self.plating_list, array_data["metal_details"]["plated"])
            self.plated_combo_box.setCurrentIndex(index)

            index = self.set_by_index_list(self.cond_list, array_data["condition"])
            self.condition_combo_box.setCurrentIndex(index)

            index = self.set_by_index_list(self.sub_gem_result, array_data["gemstone_details"]["type"])
            self.type_combo_box.setCurrentIndex(index)

            index = self.set_by_index_list(self.plat_list, array_data["store_platform"])
            self.platform_combo_box.setCurrentIndex(index)

            index = self.set_by_index_list(self.sell_status_list, array_data["sell_status"])
            self.sell_status_combo_box.setCurrentIndex(index)

            self.set_images(array_data["image_urls"])
            
            self.created_result_label.setText(array_data["date_added"])
            self.updated_result_label.setText(array_data["last_modified"])
            self.handmade_combo_box.setCurrentText(str(array_data["handmade"]))
            self.color_combo_box.setCurrentText(array_data["color"])
            self.populate_shade_dropdown()

            index = self.set_by_index_list(self.shade_list, array_data["shade"])
            self.shade_combo_box.setCurrentIndex(index)
            self.category_combo_box.setCurrentText(array_data["category"])

            # -----  Misc ----- 
            self.misc_description_box.setPlainText(array_data["notes"])

            # ----- Pricing ----- 
            self.research_pt_edit.setPlainText(str(array_data["researched_price"]))
            self.my_price_pt_edit.setPlainText(str(array_data["unit_price"]))
            self.url_pt_edit.setPlainText(array_data["listing_url"])

            # ----- Dimensions ----- 
            #    - Chain
            chain_obj_list = [self.len_pt_edit, self.width_pt_edit, self.height_pt_edit]
            self.controller_obj.process_dimensions(True, array_data["dimensions"]["chain"], chain_obj_list)

            #    - Clasp
            chain_obj_list = [self.clasp_len_pt_edit, self.clasp_width_pt_edit, self.clasp_height_pt_edit]
            self.controller_obj.process_dimensions(True, array_data["dimensions"]["clasp"], chain_obj_list)

            #    - Focal
            chain_obj_list = [self.focal_len_pt_edit, self.focal_width_pt_edit, self.focal_height_pt_edit]
            self.controller_obj.process_dimensions(True, array_data["dimensions"]["focal"], chain_obj_list)

            #    - Focal
            chain_obj_list = [self.pin_len_pt_edit, self.pin_width_pt_edit]
            self.controller_obj.process_dimensions(False, array_data["dimensions"]["pin"], chain_obj_list)

            # Status
            self.photo_checkbox.setChecked(array_data["status"]["photo"])
            self.measure_checkbox.setChecked(array_data["status"]["measuring"])
            self.cleaning_checkbox.setChecked(array_data["status"]["cleaning"])
            self.repair_checkbox.setChecked(array_data["status"]["repairing"])
            self.weighing_checkbox.setChecked(array_data["status"]["weighing"])
            self.listed_checkbox.setChecked(array_data["status"]["listing"])
            self.boxing_checkbox.setChecked(array_data["status"]["boxing"])
            self.label_location_pt_edit.setPlainText(array_data["label_location"])

    def set_images(self, img_list_data):
        list_of_imgs = [self.image_label1, self.image_label2, self.image_label3,
                        self.image_label4, self.image_label5, self.image_label6]
        for img in list_of_imgs:
            img.clear()

        if img_list_data:
            for i, image in enumerate(img_list_data):
                if i == 6:
                    break
                elif i == 0:
                    img_directory = os.path.dirname(img_list_data[0])
                    self.images_directory_pt_edit.setPlainText(img_directory)
                    pixmap = QtGui.QPixmap(image)
                    self.image_label1.setPixmap(pixmap)
                    self.image_label1.setScaledContents(True)
                elif i == 1:
                    pixmap = QtGui.QPixmap(image)
                    self.image_label2.setPixmap(pixmap)
                    self.image_label2.setScaledContents(True)
                elif i == 2:
                    pixmap = QtGui.QPixmap(image)
                    self.image_label3.setPixmap(pixmap)
                    self.image_label3.setScaledContents(True)
                elif i == 3:
                    pixmap = QtGui.QPixmap(image)
                    self.image_label4.setPixmap(pixmap)
                    self.image_label4.setScaledContents(True)
                elif i == 4:
                    pixmap = QtGui.QPixmap(image)
                    self.image_label5.setPixmap(pixmap)
                    self.image_label5.setScaledContents(True)
                elif i == 5:
                    pixmap = QtGui.QPixmap(image)
                    self.image_label6.setPixmap(pixmap)
                    self.image_label6.setScaledContents(True)

    def set_by_index_dict(self, data_list, expected, key):
        if expected:
            for index, dictionary in enumerate(data_list):
                if dictionary[key] == expected.lower():
                    return index+1
        else:
            return 0

    def print_data_label(self):
        name = self.name_pt_edit.toPlainText()
        price = self.my_price_pt_edit.toPlainText()
        brand = self.manuf_pt_edit.toPlainText()
        sku = self.sku_pt_edit.toPlainText()
        checkboxes = []
        for val in self.checkboxes:
            is_checked = val.isChecked()
            checkboxes.append(is_checked)
        created = self.created_result_label.text()
        location = self.label_location_pt_edit.toPlainText()
        self.controller_obj.create_label_grid(name,
                                              price,
                                              brand,
                                              sku,
                                              checkboxes,
                                              created,
                                              location)
        filter_text = "product.sku"
        val = sku
        dictionary = {"product.$.label_location" : location}
        self.model_obj.update_generic_data(filter_text, val, dictionary)

        dictionary2 = {"product.$.label_printed" : "Yes"}
        self.model_obj.update_generic_data(filter_text, val, dictionary2)
        self.print_stat_result_label.clear()
        self.print_stat_result_label.setText("<font color='green'>" + "Yes" + "</font>")
        

    def on_date_selected(self, date):
        self.posted_pt_edit.setPlainText(date.toString(QtCore.Qt.ISODate))
        self.calendar.hide()

    def show_calendar(self, event):
        # Position the calendar below the QPlainTextEdit
        calendar_pos = self.posted_pt_edit.mapToGlobal(event.pos())
        calendar_x = calendar_pos.x() - 600
        calendar_y = calendar_pos.y()- 40
        self.calendar.resize(400, 300)

        # Move the calendar to the desired position and show it
        self.calendar.move(calendar_x, calendar_y)
        self.calendar.show()

    def set_by_index_list(self, data_list, expected):
        if expected:
            data_list = [x.lower() for x in data_list]
            return data_list.index(expected.lower())
        else:
            return 0

    def populate_table(self, data):
        headers = list(data[0].keys())
        self.jewel_table.setColumnCount(len(headers))
        self.jewel_table.setHorizontalHeaderLabels(headers)
        self.jewel_table.setRowCount(len(data))

        for row, item in enumerate(data):
            self.jewel_table.setRowHeight(row, 80)
            for col, key in enumerate(headers):
                if col == 0:
                    icon = QtGui.QIcon(item["image"])
                    self.jewel_table.setItem(row, col, QtWidgets.QTableWidgetItem(icon, ""))
                    self.jewel_table.setIconSize(QtCore.QSize(80, 80))
                elif key == "shop_status":
                    status = self.controller_obj.process_status_table(item[key])
                    table_item = QtWidgets.QTableWidgetItem(status.capitalize())
                    table_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.jewel_table.setItem(row, col, table_item)
                else:
                    table_item = QtWidgets.QTableWidgetItem(str(item[key]))
                    table_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.jewel_table.setItem(row, col, table_item)

    def open_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ExistingFile

        found_file = False
        while found_file is False:
            file_names, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select Files", "", "Image Files (*.png *.jpg);;All Files (*)", options=options)

            valid_files = [file for file in file_names if file.endswith((".png", ".jpg"))]
            if valid_files:
                print("Selected files:", valid_files)
                final_list, query_val, query_key = self.controller_obj.handle_imgs(self.sku_pt_edit.toPlainText(),
                                                                                   self.name_pt_edit.toPlainText(),
                                                                                   valid_files)
                self.model_obj.update_imgs(query_key, query_val, final_list)

                if not final_list:
                    self.show_error_popup("Please provide the SKU or exact name of the product to upload images to!")
                else:
                    self.set_images(final_list)
                found_file = True
                break
            else:
                self.show_error_popup("All selected files must be PNG or JPG!")
                break

    def open_file_label_dialog(self, pt_obj):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            pt_obj.setPlainText(directory)
        else:
            print("No directory selected or dialog was canceled")
            pt_obj.clear()

    def show_error_popup(self, err_msg):
        # Create the error popup using QMessageBox
        error_message = QtWidgets.QMessageBox(self)
        error_message.setIcon(QtWidgets.QMessageBox.Critical)  # Set the icon to critical (error)
        error_message.setWindowTitle("Error")
        error_message.setText("An error occurred!")
        error_message.setInformativeText(err_msg)
        error_message.setStandardButtons(QtWidgets.QMessageBox.Ok)
        error_message.resize(400, 200)
        error_message.exec_()  # Display the popup

    def highlight_row(self):
        # Clear the previous highlights
        for row in range(self.jewel_table.rowCount()):
            for col in range(self.jewel_table.columnCount()):
                item = self.jewel_table.item(row, col)
                if item:
                    item.setBackground(QtGui.QColor(255, 255, 255))  # Reset to default color

        # Get the selected row indices
        selected_rows = self.jewel_table.selectionModel().selectedRows()

        # Highlight the selected row
        for selected_row in selected_rows:
            row = selected_row.row()
            for col in range(self.jewel_table.columnCount()):
                item = self.jewel_table.item(row, col)
                if item:
                    item.setBackground(QtGui.QColor(173, 216, 230))

    def show_dropdown(self):
        """ Display the popup to close after selection """
        print("Displaying Condition Options")
        self.condition_combo_box.hidePopup()
    
    def shade_dropdown(self):
        """ Set the shade hex color in the display box """
        selected_text = self.shade_combo_box.currentText().lower()
        hex_num = None
        for value in self.large_shade_list:
            if selected_text == value["name"].lower():
                hex_num = value["hex"]
                break
        if hex_num:
            self.color_display.setStyleSheet("QGroupBox { background-color: " + hex_num + "; }")

    def shade_query(self, selected_text):
        """ Getter for querying for shades
            Args:
                selected_text (str) : Color selected from color_combo_box
        """
        return self.model_obj.shade_query(selected_text)

    def populate_shade_dropdown(self):
        """ Retrieve shades from the selected color """
        print("Displaying Shade Options")
        selected_text = self.color_combo_box.currentText().lower()
        if not selected_text == '':
            result = self.shade_query(selected_text)
            self.shade_combo_box.setEnabled(True)
            self.shade_combo_box.clear()
            wee = result[0]
            self.large_shade_list = wee.get("colors", {}).get(selected_text, {}).get("shades", [])
            self.shade_list = [d['name'] for d in self.large_shade_list]
            self.shade_list.insert(0, "")
            self.shade_combo_box.addItems(self.shade_list)
        else:
            self.shade_combo_box.clear()
            self.shade_combo_box.setEnabled(False)
        
        self.color_combo_box.hidePopup()

    def populate_subgem_dropdown(self):
        """ Retrieve gem types from the selected color """
        print("Displaying Shade Options")
        selected_text = self.gemstone_combo_box.currentText().lower()
        if not selected_text == '':
            self.sub_gem_result = self.controller_obj.process_subgemstones(self.gem_list, selected_text)
            self.type_combo_box.setEnabled(True)
            self.type_combo_box.clear()
            self.sub_gem_result.insert(0, "")
            self.type_combo_box.addItems(self.sub_gem_result)
        else:
            self.type_combo_box.clear()
            self.type_combo_box.setEnabled(False)
        
        self.color_combo_box.hidePopup()

    def color_query(self):
        """ Getter to query available colors """
        return self.model_obj.color_query()

    def product_query(self):
        """ Getter to query available products """
        return self.model_obj.product_query()
    
    def condition_query(self):
        """ Getter to query available conditions """
        return self.model_obj.condition_query()
    
    def category_query(self):
        """ Getter to query available conditions """
        return self.model_obj.category_query()
    
    def gem_query(self):
        """ Getter to query available gemstones """
        return self.model_obj.gem_query()

    def clarity_query(self):
        """ Getter to query available clarity """
        return self.model_obj.clarity_query()

    def cut_query(self):
        """ Getter to query available cuts """
        return self.model_obj.cut_query()
    
    def metal_query(self):
        """ Getter to query available metal """
        return self.model_obj.metal_query()
    
    def plating_query(self):
        """ Getter to query available plating """
        return self.model_obj.plating_query()
    
    def subcategory_query(self):
        """ Getter to query available subcategory """
        return self.model_obj.subcategory_query()
    
    def platforms_query(self):
        """ Getter to query available platforms """
        return self.model_obj.platforms_query()
    
    def sell_status_query(self):
        """ Getter to query available sell status """
        return self.model_obj.sell_status_query()

    def sku_query(self, sku):
        """ Getter to query available sku """
        return self.model_obj.sku_query(sku)

    def clicked_log(self, elementName):
        print("{} clicked!", elementName)

    def get_list_widget_items(self):
        items = []
        for index in range(self.tag_list_widget.count()):
            item = self.tag_list_widget.item(index)
            items.append(item.text())
        return items

    def on_tab_save(self):
        if not self.name_pt_edit.toPlainText() and not self.sku_pt_edit.toPlainText():
            print("Nothing to save!")
            return
        tags = self.get_list_widget_items()
        final_list, query_val, query_key = self.controller_obj.handle_imgs(self.sku_pt_edit.toPlainText(),
                                                                                   self.name_pt_edit.toPlainText(),
                                                                                   [])
        # Get current datetime in UTC
        current_datetime_utc = datetime.utcnow()

        # Format the datetime to the desired string format
        formatted_datetime = current_datetime_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        # tags = [self.tag_list_widget.item(i).text() for i in range(self.tag_list_widget.count())]

        if not self.created_result_label.text():
            create_time = formatted_datetime
        else:
            create_time = self.created_result_label.text()

        data_dict = {
            "product_name" : self.name_pt_edit.toPlainText(),
            "category" : self.category_combo_box.currentText(),
            "subcategory" : self.sub_category_combo_box.currentText(),
            "color" : self.color_combo_box.currentText(),
            "shade" : self.shade_combo_box.currentText(),
            "condition" : self.condition_combo_box.currentText(),
            "handmade" : self.handmade_combo_box.currentText(),
            "store_platform" : self.platform_combo_box.currentText(),
            "sku" : self.sku_pt_edit.toPlainText(),
            "quantity_in_stock" : self.quan_pt_edit.toPlainText(),
            "unit_price" : self.my_price_pt_edit.toPlainText(),
            "researched_price" : self.research_pt_edit.toPlainText(),
            "sell_status" : self.sell_status_combo_box.currentText(),
            "label_printed" : self.print_stat_result_label.text(),
            "gemstone": self.gemstone_combo_box.currentText(),
            "gemstone_details": {
                "cut": self.cut_combo_box.currentText(),
                "clarity": self.clarity_combo_box.currentText(),
                "carat_weight": self.carat_gem_pt_edit.toPlainText(),
                "type": self.type_combo_box.currentText()
            },
            "metal_type": self.metal_combo_box.currentText(),
            "metal_details": {
                "carats" : self.carat_pt_edit.toPlainText(),
                "plated" : self.plated_combo_box.currentText()
            },
            "dimensions" : 
            {
                "chain" : {
                    "length" : self.len_pt_edit.toPlainText(),
                    "width" : self.width_pt_edit.toPlainText(),
                    "height" : self.height_pt_edit.toPlainText()
                },
                "clasp" : {
                    "length" : self.clasp_len_pt_edit.toPlainText(),
                    "width" : self.clasp_width_pt_edit.toPlainText(),
                    "height" : self.clasp_height_pt_edit.toPlainText()
                },
                "focal" : {
                    "length" : self.focal_len_pt_edit.toPlainText(),
                    "width" : self.focal_width_pt_edit.toPlainText(),
                    "height" : self.focal_height_pt_edit.toPlainText()
                },
                "pin" : {
                    "length" : self.pin_len_pt_edit.toPlainText(),
                    "width" : self.pin_width_pt_edit.toPlainText()
                }
            },
            "weight_before": self.weight_after_pt_edit.toPlainText(),
            "weight_after": self.weight_after_pt_edit.toPlainText(),
            "brand": self.manuf_pt_edit.toPlainText(),
            "date_added": create_time,
            "last_modified": formatted_datetime,
            "date_posted" : self.posted_pt_edit.toPlainText(),
            "tags" : tags,
            "image_urls" : final_list,
            "status" : {
                "photo" : self.photo_checkbox.isChecked(),
                "measuring" : self.measure_checkbox.isChecked(),
                "cleaning" : self.cleaning_checkbox.isChecked(),
                "repairing" : self.repair_checkbox.isChecked(),
                "weighing" : self.weighing_checkbox.isChecked(),
                "listing" : self.listed_checkbox.isChecked(),
                "boxing" : self.boxing_checkbox.isChecked()
            },
            "listing_url" : self.url_pt_edit.toPlainText(),
            "notes" : self.misc_description_box.toPlainText(),
            "label_location" : self.label_location_pt_edit.toPlainText()
        }

        self.model_obj.update_data(self.sku_pt_edit.toPlainText(),
                                   self.name_pt_edit.toPlainText(),
                                   data_dict)
        
        self.product_list = self.product_query()
        table_data = self.controller_obj.process_products(self.product_list)
        self.populate_table(table_data)

    def on_upload_image(self):
        print("ope")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())