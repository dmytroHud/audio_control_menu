import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from pulsectl import Pulse
from Xlib import display

class AudioControlWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Audio Control")
        self.setGeometry(100, 100, 300, 10)
        
        self.set_custom_wm_class("CustomMixer", "CustomMixer")

        self.pulse = Pulse('volume-control')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_streams)
        self.timer.start(1000)  # Update every 1 second (adjust as needed)

        self.setStyleSheet("background-color: #2f343f; color: #D0CFCC")

        self.layout = QVBoxLayout()
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # Initial update
        self.update_streams()

    def update_streams(self):
        # Clear previous widgets
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            widget.setParent(None)
        
        # Get current list of playback streams
        for stream in self.pulse.sink_input_list():
            stream_widget = self.create_stream_widget(stream)
            self.layout.addWidget(stream_widget)

    def create_stream_widget(self, stream):
        widget = QWidget()
        h_layout = QHBoxLayout()

        # Application name label on the left
        label = QLabel(f"{stream.proplist.get('application.name', 'Unknown')} (ID: {stream.index})")
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("margin-top: 10px;")

        # Mute/Unmute button on the right
        mute_button = QPushButton("Mute" if not stream.mute else "Unmute")
        mute_button.setCheckable(True)
        mute_button.setChecked(stream.mute)
        mute_button.clicked.connect(lambda checked, s=stream: self.toggle_mute(s, mute_button))

        mute_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin-top: 0;
                border-radius: 4px;
            }
            QPushButton:checked {
                background-color: #f44336; /* Red */
            }
        """)

        # Add widgets to horizontal layout
        h_layout.addWidget(label)
        h_layout.addStretch()
        h_layout.addWidget(mute_button)
        h_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Align widgets within the layout

        widget.setLayout(h_layout)
        return widget

    def toggle_mute(self, stream, button):
        self.pulse.mute(stream, not stream.mute)
        button.setText("Mute" if not stream.mute else "Unmute")

    def set_custom_wm_class(self, wm_name, wm_class):
        d = display.Display()
        w = d.create_resource_object('window', int(self.winId()))
        w.set_wm_name(wm_name)
        w.set_wm_class(wm_class, wm_class)
        d.flush()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioControlWindow()
    window.show()
    sys.exit(app.exec_())
