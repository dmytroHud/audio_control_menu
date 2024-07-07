import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import QTimer
import subprocess

class PlayerControlWidget(QWidget):
    def __init__(self, player_id, player_info, parent=None):
        super().__init__(parent)
        self.pause_icon = ""
        self.play_icon = ""

        self.player_id = player_id
        self.player_info = player_info

        layout = QHBoxLayout()
        self.setLayout(layout)
        self.label = QLabel(self.player_info['meta'])
        layout.addWidget(self.label)


        self.print_pause_play_button(layout)

    def toggle_player(self):
        try:
            output = subprocess.check_output(['playerctl', '-p', self.player_id, 'status'])
            status = output.decode('utf-8').strip()

            if status == "Playing":
                subprocess.run(['playerctl', '-p', self.player_id, 'pause'])
                self.pause_play_button.setText(self.play_icon)
            else:
                subprocess.run(['playerctl', '-p', self.player_id, 'play'])
                self.pause_play_button.setText(self.pause_icon)

        except subprocess.CalledProcessError:
            pass

    def print_pause_play_button(self, layout):
        self.pause_play_button = QPushButton()
        self.pause_play_button.setFixedWidth(45)
        self.pause_play_button.setStyleSheet("""
            QPushButton {
                background-color: #5E5C64; /* Green */
                border: none;
                color: white;
                width: 45px;
                text-align: center;
                text-decoration: none;
                font-size: 26px;
                margin-top: 0;
                border-radius: 4px;
            }
        """)
        self.pause_play_button.setText(self.pause_icon if "Playing" in self.player_info['status'] else self.play_icon)
        self.pause_play_button.clicked.connect(self.toggle_player)
        layout.addWidget(self.pause_play_button)