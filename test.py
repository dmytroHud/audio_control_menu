#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt

class TickerLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.full_text = text
        self.current_index = 0

        self.setFixedWidth(200)  # Set fixed width
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setStyleSheet("background-color: #2f343f; color: #D0CFCC; padding: 5px;")
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_text)
        self.timer.start(100)  # Update text every 100ms

    def scroll_text(self):
        display_text = self.full_text[self.current_index:] + " " + self.full_text[:self.current_index]
        self.setText(display_text)
        self.current_index = (self.current_index + 1) % len(self.full_text)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ticker Label Example')
        
        layout = QVBoxLayout()
        self.ticker_label = TickerLabel("This is a very long text that will scroll automatically like a ticker.")
        layout.addWidget(self.ticker_label)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #2f343f;")
        self.resize(300, 100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
