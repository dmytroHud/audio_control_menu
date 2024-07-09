import sys
from Ticker import Ticker
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel, QHBoxLayout, QCheckBox
from PyQt5.QtCore import QTimer, Qt
import subprocess

class PlayerControlWidget(QWidget):
    def __init__(self, player_id, player_info, parent=None):
        super().__init__(parent)
        self.pause_icon = ""
        self.play_icon = ""
        self.player_id = player_id
        self.player_info = player_info

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.print_pin_button()
        self.print_label()
        self.print_prev_button()
        self.print_pause_play_button()
        self.print_next_button()

    def toggle_player(self):
        try:
            output = subprocess.check_output(['playerctl', '-p', self.player_id, 'status'])
            status = output.decode('utf-8').strip()

            if status == "Playing":
                subprocess.run(['playerctl', '-p', self.player_id, 'pause', '2>/dev/null'])
                self.pause_play_button.setText(self.play_icon)
            else:
                subprocess.run(['playerctl', '-p', self.player_id, 'play', '2>/dev/null'])
                self.pause_play_button.setText(self.pause_icon)

        except subprocess.CalledProcessError:
            pass

    def set_pinned(self):
        subprocess.run(f"echo '{self.player_id}' > /tmp/active_player", shell=True, check=True);

    def action_next(self):
        subprocess.run(['playerctl', '-p', self.player_id, 'next', '2>/dev/null'])

    def action_previous(self):
        subprocess.run(['playerctl', '-p', self.player_id, 'previous', '2>/dev/null'])

    def print_label(self):
        if len(self.player_info['meta']) > 35:
            label = Ticker(self.player_info['meta'] + "  ♫  ")
        else:
            label = QLabel("♫  " + self.player_info['meta'])

        label.setFixedWidth(250)
        self.layout.addWidget(label)

    def print_pin_button(self):
        self.pin_button = QPushButton();
        self.pin_button.setText("☉")
        self.pin_button.setStyleSheet("""
            QPushButton {
                background-color: #5E5C64;
                border: none;
                color: white;
                text-align: center;
                text-decoration: none;
                font-size: 18px;
                margin-top: 0;
                font-weight: 700;
                border-radius: 10px;
            }
        """)
        self.pin_button.clicked.connect(self.set_pinned)
        self.layout.addWidget(self.pin_button)

    def print_pause_play_button(self):
        self.pause_play_button = QPushButton()
        self.pause_play_button.setFixedWidth(30)
        self.pause_play_button.setStyleSheet("""
            QPushButton {
                background-color: #5E5C64;
                border: none;
                color: white;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin-top: 0;
                padding-top: 1px;
                padding-bottom: 1px;
                border-radius: 4px;
            }
        """)
        self.pause_play_button.setText(self.pause_icon if "Playing" in self.player_info['status'] else self.play_icon)
        self.pause_play_button.clicked.connect(self.toggle_player)
        self.layout.addWidget(self.pause_play_button)

    def print_next_button(self):
        self.next_button = QPushButton()
        self.next_button.setFixedWidth(30)
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #5E5C64;
                border: none;
                color: white;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
                margin-top: 0;
                border-radius: 4px;
                padding-top: 2px;
                padding-bottom: 2px;
            }
        """)
        self.next_button.setText("❱")
        self.next_button.clicked.connect(self.action_next)
        self.layout.addWidget(self.next_button)

    def print_prev_button(self):
        self.prev_button = QPushButton()
        self.prev_button.setFixedWidth(30)
        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: #5E5C64;
                border: none;
                color: white;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
                margin-top: 0;
                border-radius: 4px;
                padding-top: 2px;
                padding-bottom: 2px;
            }
        """)
        self.prev_button.setText("❰")
        self.prev_button.clicked.connect(self.action_previous)
        self.layout.addWidget(self.prev_button)