import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal

class Ticker(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.full_text = text
        self.current_index = 0
        self.scroll_step = 1  # Number of characters to scroll per step

        # self.setFixedWidth(350)  # Set fixed width
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setStyleSheet("background-color: #2f343f; color: #D0CFCC; padding: 5px;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_text)
        self.timer.start(100)  # Update text every 30ms for smoother animation

    def scroll_text(self):
        display_text = self.full_text[self.current_index:] + " " + self.full_text[:self.current_index]
        self.setText(display_text)
        self.current_index = (self.current_index + self.scroll_step) % len(self.full_text)


# from PyQt5.QtWidgets import QLabel, QApplication, QVBoxLayout, QWidget
# from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty
# from PyQt5 import QtGui

# class Ticker(QLabel):
#     def __init__(self, text, parent=None):
#         super().__init__(parent)
#         self.full_text = text
#         self.setFixedWidth(200)
#         self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
#         # self.setStyleSheet("background-color: #2f343f; color: #D0CFCC;")

#         self._offset = 0
#         self.animation = QPropertyAnimation(self, b"offset")
#         self.animation.setDuration(5000)  # Duration of the scroll animation
#         self.animation.setStartValue(0)
#         self.animation.setEndValue(len(self.full_text) * self.fontMetrics().horizontalAdvance(' '))
#         self.animation.setLoopCount(-1)  # Infinite loop
#         self.animation.start()

#     @pyqtProperty(int)
#     def offset(self):
#         return self._offset

#     @offset.setter
#     def offset(self, value):
#         self._offset = value
#         self.update()

#     def paintEvent(self, event):
#         painter = QtGui.QPainter(self)
#         rect = self.rect()
#         text_width = self.fontMetrics().horizontalAdvance(self.full_text)
#         text_height = self.fontMetrics().height()
        
#         x = rect.width() - self._offset
#         y = text_height

#         # Draw text twice for continuous effect
#         painter.drawText(x, y, self.full_text)
#         painter.drawText(x + text_width + 10, y, self.full_text)



# class Ticker(QLabel):
#     def __init__(self, text, parent=None):
#         super().__init__(parent)
#         self.full_text = text
#         self.setFixedWidth(200)
#         self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

#         self._offset = 0
#         self.calculate_animation_duration()

#         self.animation = QPropertyAnimation(self, b"offset")
#         self.animation.setStartValue(0)
#         self.animation.setEndValue(len(self.full_text) * self.fontMetrics().horizontalAdvance(' '))
#         self.animation.setLoopCount(-1)  # Infinite loop
#         self.animation.setDuration(int(self.animation_duration))
#         self.animation.start()

#     def calculate_animation_duration(self):
#         # Calculate animation duration based on text length and fixed width

#         text_width = self.fontMetrics().horizontalAdvance(self.full_text)
#         pixels_per_second = 5 # Adjust this value as needed for speed
#         print(text_width, self.width())

#         self.animation_duration = text_width / self.width() * 1000

#     @pyqtProperty(int)
#     def offset(self):
#         return self._offset

#     @offset.setter
#     def offset(self, value):
#         self._offset = value
#         self.update()

#     def paintEvent(self, event):
#         painter = QtGui.QPainter(self)
#         rect = self.rect()
#         text_width = self.fontMetrics().horizontalAdvance(self.full_text)
#         text_height = self.fontMetrics().height()
        
#         x = rect.width() - self._offset
#         y = text_height

#         # Draw text twice for continuous effect
#         painter.drawText(x, y, self.full_text)
#         painter.drawText(x + text_width + 10, y, self.full_text)


# class Ticker(QLabel):
#     def __init__(self, parent=None):
#         QLabel.__init__(self, parent)
#         self.px = 0
#         self.py = 15
#         self._direction = Qt.LeftToRight
#         self.setWordWrap(True)
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update)
#         self.timer.start(40)
#         self._speed = 2
#         self.textLength = 0
#         self.fontPointSize = 0
#         self.setAlignment(Qt.AlignVCenter)
#         self.setFixedHeight(self.fontMetrics().height())

#     def setFont(self, font):
#         QLabel.setFont(self, font)
#         self.setFixedHeight(self.fontMetrics().height())

#     def updateCoordinates(self):
#         align = self.alignment()
#         if align == Qt.AlignTop:
#             self.py = 10
#         elif align == Qt.AlignBottom:
#             self.py = self.height() - 10
#         elif align == Qt.AlignVCenter:
#             self.py = self.height() / 2
#         self.fontPointSize = self.font().pointSize() / 2
#         self.textLength = self.fontMetrics().width(self.text())

#     def setAlignment(self, alignment):
#         self.updateCoordinates()
#         QLabel.setAlignment(self, alignment)

#     def resizeEvent(self, event):
#         self.updateCoordinates()
#         QLabel.resizeEvent(self, event)

#     def paintEvent(self, event):
#         painter = QtGui.QPainter(self)
#         if self._direction == Qt.RightToLeft:
#             self.px -= self.speed()
#             if self.px <= -self.textLength:
#                 self.px = self.width()
#         else:
#             self.px += self.speed()
#             if self.px >= self.width():
#                 self.px = -self.textLength
#         painter.drawText(self.px, self.py + self.fontPointSize, self.text())
#         painter.translate(self.px, 0)

#     def speed(self):
#         return self._speed

#     def setSpeed(self, speed):
#         self._speed = speed

#     def setDirection(self, direction):
#         self._direction = direction
#         if self._direction == Qt.RightToLeft:
#             self.px = self.width() - self.textLength
#         else:
#             self.px = 0
#         self.update()

#     def pause(self):
#         self.timer.stop()

#     def unpause(self):
#         self.timer.start()