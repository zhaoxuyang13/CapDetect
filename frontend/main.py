import sys
import mainWindow

from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    ui = mainWindow.Ui_Dialog()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
