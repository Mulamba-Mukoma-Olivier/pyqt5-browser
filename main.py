import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

import images_rc
from browser import Browser


QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

app = QApplication(sys.argv)

window = Browser()
window.show()

sys.exit(app.exec_())