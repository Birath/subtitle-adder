import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QLCDNumber, QSlider, \
    QVBoxLayout, QFileDialog
from PyQt5.QtCore import QCoreApplication, Qt
from subtitle_adder import add_subs_to_season


class Tut(QWidget):

    def __init__(self):
        super().__init__()
        self.video_folder = ""
        self.sub_folder = ""
        self.mkvmerge_folder = ""
        self.output_folder = ""
        self.initUI()

    def initUI(self):

        btn = QPushButton('Quit', self)
        # noinspection PyUnresolvedReferences
        btn.clicked.connect(QCoreApplication.instance().quit)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        video_btn = QPushButton("Season", self)
        video_btn.clicked.connect(lambda: self.get_folder("season"))

        sub_path_btn = QPushButton("Subtitles", self)
        sub_path_btn.clicked.connect(lambda: self.get_folder("subtitle"))

        output_folder_btn = QPushButton("Output folder", self)
        output_folder_btn.clicked.connect(lambda: self.get_folder("output"))

        path_btn = QPushButton("MkvMerge", self)
        path_btn.clicked.connect(lambda: self.get_folder("mkvmerge"))

        sub_btn = QPushButton('Sub', self)
        sub_btn.clicked.connect(lambda: add_subs_to_season(self.video_folder, self.sub_folder,
                                                           args={"video_input": self.video_folder,
                                                                 "sub_input": self.sub_folder,
                                                                 "lang": "swe", "name": "Swedish",
                                                                 "output": None, "output_folder": self.output_folder,
                                                                 "forced": False, "default": None,
                                                                 "path": self.mkvmerge_folder, "remove_input": False}))
        video_btn.move(150, 550)
        sub_path_btn.move(225, 550)
        output_folder_btn.move(300, 550)
        path_btn.move(375, 550)
        sub_btn.move(450, 550)

        self.resize(600, 600)
        self.center()

        self.setWindowTitle('Icon')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def get_folder(self, dialog):
        folder = QFileDialog.getExistingDirectory(None, "Select {} folder".format(dialog))
        if dialog == "subtitle":
            self.sub_folder = os.path.normpath(folder)
        elif dialog == "season":
            self.video_folder = os.path.normpath(folder)
        elif dialog == "mkvmerge":
            self.mkvmerge_folder = os.path.normpath(folder)
        elif dialog == "output":
            self.output_folder = os.path.normpath(folder)
        print(self.video_folder)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = Tut()

    sys.exit(app.exec_())




