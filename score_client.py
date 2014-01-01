#!/usr/bin/python

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from stats import ScoreStats


app = QApplication(sys.argv)

class ScoreView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout()
        stat = ScoreStats()

        # get win-ration of each team
        win_ratios = stat.get_win_ratio()
        for team, win_ratio in win_ratios:
            label = QLabel('%s(%d)' % (team, win_ratio), self)
            self.layout.addWidget(label)

        self.setLayout(self.layout)
        
    def run(self):
        self.show()
        app.exec_()

ScoreView().run()
