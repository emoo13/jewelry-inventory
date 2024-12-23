# TODO: This is for if mom doesn't like the resizing of the table, we can integrate this
        # self.jewel_table.setFixedWidth(1200)  # Adjust as needed
        # self.jewel_table.setFixedHeight(900)  # Adjust as needed
        # self.jewel_table.horizontalHeader().sectionResized.connect(self.adjust_columns)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

    # TODO: This is for if mom doesn't like the resizing of the table, we can integrate this
    # def adjust_columns(self):
    #     """
    #     Adjust column widths to fit within the fixed table width.
    #     If a column reaches the minimum width, the next column in order starts resizing.
    #     """
    #     total_width = self.jewel_table.width() - self.jewel_table.verticalHeader().width()
    #     remaining_width = total_width

    #     # Start resizing from the last column backward
    #     for col in reversed(range(self.jewel_table.columnCount())):
    #         current_width = self.jewel_table.columnWidth(col)
    #         new_width = max(MIN_COLUMN_WIDTH, min(current_width, remaining_width))
    #         self.jewel_table.setColumnWidth(col, new_width)
    #         remaining_width -= new_width

    #     # Ensure the remaining space doesn't leave any column too small
    #     if remaining_width > 0:
    #         for col in range(self.jewel_table.columnCount()):
    #             self.jewel_table.setColumnWidth(col, self.jewel_table.columnWidth(col) + remaining_width // self.jewel_table.columnCount())
    # def adjust_last_column(self):
    #     total_width = sum(
    #         self.jewel_table.columnWidth(c) for c in range(self.jewel_table.columnCount() - 1)
    #     )
    #     last_column_width = self.jewel_table.width() - total_width - self.jewel_table.verticalHeader().width()
    #     if last_column_width > 0:
    #         self.jewel_table.setColumnWidth(self.jewel_table.columnCount() - 1, last_column_width)
    #     else:
    #         # Prevent negative widths
    #         self.jewel_table.setColumnWidth(self.jewel_table.columnCount() - 1, 0)
