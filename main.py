import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QListWidget, QInputDialog, QListWidgetItem, QFrame, QHBoxLayout
from PySide6.QtCore import QSize
from PySide6.QtGui import QBrush, QColor


#custom frame for characters
class CharacterWidget(QFrame):
    def __init__(self, char_name, initiative_value, remove_callback):
        super().__init__()
        self.char_name = char_name
        self.initiative_value = initiative_value
        #create horizontal layout
        layout = QHBoxLayout()
        #label for character name and initiative
        self.label = QLabel(f"{self.char_name} : {self.initiative_value}")
        layout.addWidget(self.label)
        #button to remove character
        self.remove_button = QPushButton("X")
        self.remove_button.setFixedSize(QSize(20, 20))
        self.remove_button.setStyleSheet("""
            QPushButton{
                    background-color: red;
                    color: white;
                    border-radius: 10px;
                    font-size: 12px;
                    padding: 0px;
            }
            QPushButton:hover {
                background-color: darkred;}
        """
            
        )
        self.remove_button.clicked.connect(self.remove_character)
        layout.addWidget(self.remove_button)
        #set layout for widget
        self.setLayout(layout)
        #store callback to remove character
        self.remove_callback = remove_callback

    def remove_character(self):
        self.remove_callback(self.char_name)




class InitiativeTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()
        #create an empty list to store characters and their initiative
        self.characters = []
        self.current_index = 0;
        self.next_button = QPushButton('Next character')


    def init_UI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Initiative Tracker")
        layout.addWidget(self.label)
        self.initiative_list = QListWidget()
        layout.addWidget(self.initiative_list)
        self.add_button = QPushButton("Add Character")
        layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_character)
        self.next_button = QPushButton('Next Character')
        layout.addWidget(self.next_button)
        self.next_button.clicked.connect(self.next_character)
        self.setLayout(layout)
        self.setWindowTitle('Initiative Tracker')

    def add_character(self):
        char_name, ok_name = QInputDialog.getText(self, "Add Character", "Enter character name:")
        if ok_name and char_name:
            initiative_value, ok_value = QInputDialog.getInt(self, 'Add Initiative', f'Enter Initiative for {char_name}:')
            if ok_value:
                self.characters.append((char_name, initiative_value))
                #sort
                self.characters.sort(key=lambda x: x[1], reverse=True)
                #update list
                self.update_list()

    def update_list(self):
        self.initiative_list.clear()
        #add updatedd characters to list
        for index, (character, initiative_value) in enumerate(self.characters):
            #create custom widget for each character
            character_widget = CharacterWidget(character, initiative_value, self.remove_character)
            list_item = QListWidgetItem(self.initiative_list)
            list_item.setSizeHint(character_widget.sizeHint())
            self.initiative_list.addItem(list_item)
            self.initiative_list.setItemWidget(list_item, character_widget)
            #hightlight current character
            if index == self.current_index:
                list_item.setBackground(QBrush(QColor("darkgreen")))

    def remove_character(self, character_name):
        self.characters = [char for char in self.characters if char[0] != character_name]
        self.update_list()

    def next_character(self):
        self.current_index = (self.current_index + 1) %len(self.characters)
        self.update_list()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InitiativeTrackerApp()
    window.show()
    sys.exit(app.exec())




        



