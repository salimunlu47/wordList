from PyQt6.QtWidgets import QApplication
from wordlist import load_words
from mainwindow import MainWindow
import sys

if __name__ == '__main__':
    # Create the application
    app = QApplication(sys.argv)

    # Load the words
    words = load_words()

    # Create the main window and show it
    main_window = MainWindow(words)
    main_window.show()

    # Run the application
    sys.exit(app.exec())
