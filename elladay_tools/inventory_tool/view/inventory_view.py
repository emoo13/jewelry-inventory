from os import error
from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess

class AnimaticUi(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AnimaticUi,self).__init__(parent)
        self.shot_tool_tip = "wee"
        self.added_tool_top = "wee"
        
        # self.model = model
        # self.controller = controller

        self.setWindowTitle("Animatic Generator")
        self.setFixedWidth(500)
        self.setFixedHeight(600)
        self.setup_ui()

        # self.on_cancel_click()
        self.on_set_project()
        self.on_set_sequence()
        self.on_set_episode()
        self.on_add_click()
        self.on_remove_click()
        self.on_create_click()
        self.ERROR = "ERROR"

    def setup_ui(self):
        window_vertical_layout = QtWidgets.QVBoxLayout(self)
        self.setup_filename(window_vertical_layout)
        self.setup_body(window_vertical_layout)
        
        self.setup_console_label(window_vertical_layout)
        self.setup_footer(window_vertical_layout)

    def setup_filename(self, parent_layout):
        file_name_group_box = QtWidgets.QGroupBox("Output Filename")
        
        filename_hor_layout = QtWidgets.QHBoxLayout(file_name_group_box)

        self.movie_name_field = QtWidgets.QLineEdit()

        filename_hor_layout.addWidget(self.movie_name_field)

        parent_layout.addWidget(file_name_group_box)

    def setup_body(self, parent_layout):
        horizontal_layout = QtWidgets.QHBoxLayout()
        vertical_layout = QtWidgets.QVBoxLayout()

        self.setup_project_combo(vertical_layout)
        self.setup_episode_combo(vertical_layout)
        self.setup_sequence_combo(vertical_layout)
        
        self.setup_shots_list(vertical_layout)
        horizontal_layout.addLayout(vertical_layout)

        self.setup_buttons(horizontal_layout)
        self.setup_added_shots_list(horizontal_layout)
        parent_layout.addLayout(horizontal_layout)

        horizontal_layout.setStretch(0, 1)
        horizontal_layout.setStretch(1, 2)
        horizontal_layout.setStretch(2, 2)
        parent_layout.addLayout(horizontal_layout)

    def setup_footer(self, parent_layout):
        buttons_horizontal_layout = QtWidgets.QHBoxLayout()
        
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        self.create_button = QtWidgets.QPushButton("Create and Open")
    
        buttons_horizontal_layout.addWidget(self.cancel_button)
        buttons_horizontal_layout.addWidget(self.create_button)
        
        parent_layout.addLayout(buttons_horizontal_layout)

    def setup_project_combo(self, parent_layout):
        project_horizontal_layout = QtWidgets.QHBoxLayout()

        self.project_label = QtWidgets.QLabel("Project")
        
        self.project_combo_box = QtWidgets.QComboBox()
        self.project_combo_box.setFixedSize(150,30)
        
        project_horizontal_layout.addWidget(self.project_label)
        project_horizontal_layout.addWidget(self.project_combo_box)
        parent_layout.addLayout(project_horizontal_layout)

        # Populate this combobox with projects from SG
        # projects = self.controller.populate_projects()
        self.project_combo_box.clear()
        self.project_combo_box.addItem("")
        # self.project_combo_box.addItems(projects)

    def setup_episode_combo(self, parent_layout):
        episode_horizontal_layout = QtWidgets.QHBoxLayout()
        
        self.episode_label = QtWidgets.QLabel("Episode")

        self.episode_combo_box = QtWidgets.QComboBox()
        self.episode_combo_box.setFixedSize(150,30)
        
        episode_horizontal_layout.addWidget(self.episode_label)
        episode_horizontal_layout.addWidget(self.episode_combo_box)
        parent_layout.addLayout(episode_horizontal_layout)

    def setup_sequence_combo(self, parent_layout):
        sequence_horizontal_layout = QtWidgets.QHBoxLayout()

        self.sequence_label = QtWidgets.QLabel("Sequence")
        
        self.sequence_combo_box = QtWidgets.QComboBox()
        self.sequence_combo_box.setFixedSize(150,30)

        sequence_horizontal_layout.addWidget(self.sequence_label)
        sequence_horizontal_layout.addWidget(self.sequence_combo_box)
        parent_layout.addLayout(sequence_horizontal_layout)

    def setup_shots_list(self, parent_layout):
        available_shots_group_box = QtWidgets.QGroupBox("Available Shots")
        shots_vertical_layout = QtWidgets.QVBoxLayout(available_shots_group_box)

        self.shot_list_widget = QtWidgets.QListWidget(available_shots_group_box)
        self.shot_list_widget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
            )
        self.shot_list_widget.setToolTip(self.shot_tool_tip)

        shots_vertical_layout.addWidget(self.shot_list_widget)
        parent_layout.addWidget(available_shots_group_box)
    
    def setup_buttons(self, parent_layout):
        button_vertical_layout = QtWidgets.QVBoxLayout()

        self.add_shot_button = QtWidgets.QPushButton(">>")
        self.add_shot_button.setFixedSize(33,130)
        button_vertical_layout.addWidget(self.add_shot_button)

        self.remove_shot_button = QtWidgets.QPushButton("<<")
        self.remove_shot_button.setFixedSize(33,130)
        button_vertical_layout.addWidget(self.remove_shot_button)
        parent_layout.addLayout(button_vertical_layout)

    def setup_added_shots_list(self, parent_layout):
        added_shots_group_box = QtWidgets.QGroupBox("Added Shots")
        added_shots_vertical_layout = QtWidgets.QVBoxLayout(added_shots_group_box)

        self.added_shots_list_widget = QtWidgets.QListWidget(
            added_shots_group_box
            )
        self.added_shots_list_widget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
            )
        self.added_shots_list_widget.setDragDropMode(
            QtWidgets.QAbstractItemView.InternalMove
            )
        self.added_shots_list_widget.setToolTip(self.added_tool_top)
        added_shots_vertical_layout.addWidget(self.added_shots_list_widget)
        parent_layout.addWidget(added_shots_group_box)

    def setup_console_label(self, parent_layout):
        console_vertical_layout = QtWidgets.QVBoxLayout()
        self.message_label = QtWidgets.QLabel()
        
        console_vertical_layout.addWidget(self.message_label)
        parent_layout.addLayout(console_vertical_layout)

# ----- Set Calls -----
    def on_set_project(self):
        self.project_combo_box.currentIndexChanged.connect(self.set_episode_combo)

    # def on_cancel_click(self):
        # self.cancel_button.clicked.connect(self.controller.cancel_button_clicked)

    def on_set_sequence(self):
        self.sequence_combo_box.currentIndexChanged.connect(self.set_shot_combo)
    
    def on_set_episode(self):
        self.episode_combo_box.currentIndexChanged.connect(self.set_sequence_combo)
    
    def on_add_click(self):
        self.add_shot_button.clicked.connect(self.set_add_button)

    def on_remove_click(self):
        self.remove_shot_button.clicked.connect(self.set_remove_shot_button)
    
    def on_create_click(self):
        self.create_button.clicked.connect(self.set_create_button)

# ----- Setters -----
    def set_message(self, message, message_type=None):
        self.message_label.clear()
        self.message_label.setText(message)
        if message_type == self.ERROR:
            self.message_label.setStyleSheet(
                'QLabel {color: #e32636; font-size: 9pt;}'
                )
        else:
            self.message_label.setStyleSheet(
                'QLabel {color: green; font-size: 9pt;}'
            )

    def set_episode_combo(self):
        project_name = self.project_combo_box.currentText()
        
        # episode_list = self.controller.populate_episodes(project_name)
        self.episode_combo_box.clear()
        # if not episode_list:
        #     # If there are no episodes for a project, the combobox will
        #     # disable, and instead populate the sequence combo box
        #     self.episode_combo_box.setEnabled(False)
        #     self.set_sequence_combo()
        # else:
        #     self.episode_combo_box.setEnabled(True)
        #     self.episode_combo_box.addItem("")
        #     self.episode_combo_box.addItems(episode_list)

    # Setter for if there are no episodes for a project
    def set_sequence_combo(self):
        episode_name = self.episode_combo_box.currentText()
        # if episode_name:
        #     sequence_list = self.controller.populate_sequences(episode_name)
        # else:
        #     sequence_list = self.controller.populate_ind_sequences()
        
        # Populate this combobox with sequences from the selected project in SG
        self.sequence_combo_box.clear()
        self.sequence_combo_box.addItem("")
        # self.sequence_combo_box.addItems(sequence_list)

    def set_shot_combo(self):
        self.shot_list_widget.clear()
        sequence_name = self.sequence_combo_box.currentText()
        
        if not sequence_name:
            return

        # try:
            # self.shots_list = self.controller.populate_shots(sequence_name)
        # except Exception:
        #     error_message = "Couldn't find shots for {sequence}".format(sequence=sequence_name)
        #     self.set_message(error_message, self.ERROR)
        #     return
            
        self.shot_list_widget.addItems(self.shots_list)

    def set_add_button(self):
        shot_selection = []
        shot_indexes = [
            item.row() for item in self.shot_list_widget.selectedIndexes()
            ]

        for shot in range(len(shot_indexes)):
            shot_selection.append(self.shots_list[int(shot_indexes[shot])])
            org_shot_selection = sorted(shot_selection)
        
        try:
            self.added_shots_list_widget.addItems(org_shot_selection)
        except Exception:
            error_message = "eep"
            self.set_message(error_message, self.ERROR)
            return

        self.message_label.clear()
            
    def set_remove_shot_button(self):
        shot_remove_indexes = [
            item.row() for item in self.added_shots_list_widget.selectedIndexes()
            ]
        
        try:
            shot_remove_indexes[0]
        except IndexError:
            error_message = "ope"
            self.set_message(error_message, self.ERROR)
            return
            
        org_shot_selection = sorted(shot_remove_indexes, reverse=True)

        if len(org_shot_selection) == self.added_shots_list_widget.count():
            self.added_shots_list_widget.clear()
        else:
            for item in range(len(org_shot_selection)):
                self.added_shots_list_widget.takeItem(org_shot_selection[item])
        self.message_label.clear()

    def set_create_button(self):
        items = []
        project_name = ""
        episode_name = ""
        sequence_name = ""
        for index_shots in range(self.added_shots_list_widget.count()):
             items.append(self.added_shots_list_widget.item(index_shots))
        labels = [i.text() for i in items]

        output_filename = str(self.movie_name_field.text()).replace(" ", "")
        if output_filename:
            self.movie_filename = output_filename
        else:
            episode = str(self.episode_combo_box.currentText())
            sequence = str(self.sequence_combo_box.currentText())
            project = str(self.project_combo_box.currentText()).replace(" ", "")
            
            if project:
                project_name = project + "_"                
            if episode:
                episode_name = episode + "_"
            else:
                episode_name = ""
            if sequence:
                sequence_name = sequence
            self.movie_filename = project_name + episode_name + sequence_name
            
        # try:
        #     self.animatic_creator = self.controller.create_movie(labels, self.movie_filename)
        # except Exception:
        #     error_message = "huh"
        #     self.set_message(error_message, self.ERROR)
        #     return
                
        success_message = "yep".format(animatic_location=self.animatic_creator)
        self.message_label.setWordWrap(True)
        self.set_message(success_message)
        # self.launch_movie()

    # def launch_movie(self):
    #     subprocess.Popen([RV_EXECUTABLE, "-play", self.animatic_creator])