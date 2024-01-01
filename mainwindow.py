from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMenu, QMenuBar, QLineEdit, \
    QMessageBox, QInputDialog, QRadioButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
import random
from wordlist import Word, insert_word, load_words


class MainWindow(QWidget):
    def __init__(self, words):
        super().__init__()
        self.words = words
        self.current_level = None

        # Set up the layout
        self.layout = QVBoxLayout()

        # Create difficulty level selection
        self.level_layout = QHBoxLayout()
        self.radio_easy = QRadioButton("Easy")
        self.radio_medium = QRadioButton("Medium")
        self.radio_hard = QRadioButton("Hard")
        self.level_layout.addWidget(self.radio_easy)
        self.level_layout.addWidget(self.radio_medium)
        self.level_layout.addWidget(self.radio_hard)

        # Connect radio buttons to a function
        self.radio_easy.toggled.connect(lambda: self.set_level("easy"))
        self.radio_medium.toggled.connect(lambda: self.set_level("medium"))
        self.radio_hard.toggled.connect(lambda: self.set_level("hard"))

        # Add the level selection to the main layout
        self.layout.addLayout(self.level_layout)

        # Create the word label and add it to the layout
        self.label_word = QLabel()
        self.label_word.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_word)

        # Create the meaning label and add it to the layout
        self.label_meaning = QLabel()
        self.label_meaning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_meaning)

        # Create the "Show Meaning" button and add it to the layout
        self.button_show_meaning = QPushButton('Show Meaning')
        self.button_show_meaning.clicked.connect(self.show_meaning)
        self.layout.addWidget(self.button_show_meaning)

        # Create the "Next Word" button and add it to the layout
        self.button_next = QPushButton('Next Word')
        self.button_next.clicked.connect(self.show_random_word)
        self.layout.addWidget(self.button_next)

        # Create the menu
        self.menu = QMenu()
        self.menu_insert_word = QAction('Insert Word', self)
        self.menu_show_word = QAction('Show Word for Learning', self)
        self.menu.addAction(self.menu_insert_word)
        self.menu.addAction(self.menu_show_word)

        # Connect menu actions
        self.menu_insert_word.triggered.connect(self.insert_word_dialog)
        self.menu_show_word.triggered.connect(self.show_meaning)

        # Create the menu button and add it to the layout
        self.button_menu = QPushButton('Menu')
        self.button_menu.setMenu(self.menu)
        self.layout.addWidget(self.button_menu)

        # Apply the layout to the widget
        self.setLayout(self.layout)

        # Show a random word to start
        self.show_random_word()

        # Set up styles
        self.setup_styles()

    def setup_styles(self):
        """Defines the styles for the buttons and labels."""
        self.label_word.setStyleSheet("QLabel { color : blue; font-size: 30px; }")
        self.label_meaning.setStyleSheet("QLabel { color : green; font-size: 20px; }")
        self.button_show_meaning.setStyleSheet("QPushButton { background-color: yellow; font-size: 20px; }")
        self.button_next.setStyleSheet("QPushButton { background-color: cyan; font-size: 20px; }")
        self.button_menu.setStyleSheet("QPushButton { background-color: lightgray; font-size: 20px; }")

    def show_random_word(self):
        """Chooses a random word from the selected level and displays it, clearing the meaning."""
        if self.current_level:
            level_words = [word for word in self.words if word.level == self.current_level]
            if level_words:
                self.word = random.choice(level_words)
                self.label_word.setText(self.word.word)
                self.label_meaning.clear()
            else:
                QMessageBox.warning(self, 'Warning', f'No words available for level: {self.current_level}')
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a difficulty level.')

    def show_meaning(self):
        """Displays the meaning of the current word."""
        if hasattr(self, 'word'):
            self.label_meaning.setText(self.word.meaning)
        else:
            QMessageBox.warning(self, 'Warning', 'No word to show meaning.')

    def insert_word_dialog(self):
        """Displays a dialog for inserting a new word."""
        word, ok = QInputDialog.getText(self, 'Insert Word', 'Enter Word:')
        if ok and word:
            meaning, ok = QInputDialog.getText(self, 'Insert Word', 'Enter Meaning:')
            if ok and meaning:
                level, ok = QInputDialog.getItem(self, 'Insert Word', 'Select Level:', ['easy', 'medium', 'hard'], 0,
                                                 False)
                if ok:
                    new_word = Word(word, meaning, level)
                    insert_word(new_word)
                    self.words = load_words()
                    self.show_random_word()

    def set_level(self, level):
        """Sets the current difficulty level."""
        self.current_level = level
        self.show_random_word()
