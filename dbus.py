import sys
from PlayerControlWidget import PlayerControlWidget
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import QTimer
import subprocess

class PlayerInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #2f343f; color: #D0CFCC")
        self.players_info = {}
        self.setWindowTitle('Player Info')
        self.layout = QVBoxLayout()
        self.player_list = QListWidget()
        self.layout.addWidget(self.player_list)
        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_player_info)
        self.timer.start(1000)

    def update_player_info(self):
        # Clear previous items
        self.player_list.clear()
        self.players_info.clear()

        # Get current players using playerctl
        try:
            players_raw = subprocess.check_output(['playerctl', '-l'])
            players = players_raw.decode('utf-8').strip().split('\n')

            for player_id in players:
                output = subprocess.check_output(['playerctl', '-p', player_id, 'metadata', '--format', '{{artist}} - {{title}}'])
                status = subprocess.check_output(['playerctl', '-p', player_id, 'status'])

                player_info = output.decode('utf-8').strip()
                status_info = status.decode('utf-8').strip()

                self.players_info[player_id] = {
                    "meta": player_info,
                    "status": status_info
                }

            self.print_players_controls()
        except subprocess.CalledProcessError:
            # Handle error (playerctl not installed or no players found)
            self.player_list.addItem('No players found')

    def print_players_controls(self):
        for player_id, player_info in self.players_info.items():
            item = QListWidgetItem(self.player_list)
            widget = PlayerControlWidget(player_id, player_info)
            item.setSizeHint(widget.sizeHint())  # Ensure proper sizing of the widget
            self.player_list.setItemWidget(item, widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PlayerInfoWidget()
    widget.show()
    sys.exit(app.exec_())
