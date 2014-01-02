#!/usr/bin/python

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from stats import ScoreStats


app = QApplication(sys.argv)

class ScoreView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.grid = QGridLayout()
        self.stat = ScoreStats()

        # add best stats to the grid
        self.grid.addWidget(self.get_table_view('best-attacks'), 0, 0)
        self.grid.addWidget(self.get_table_view('best-defences'), 0, 1)
        self.grid.addWidget(self.get_table_view('win-ratios'), 1, 0)
        self.grid.addWidget(self.get_table_view('goalscorers'), 1, 1)
        self.setLayout(self.grid)

    def get_table_view(self, stat_type):
        """ Returns the table view, of the given stat type

            Args:
                stat_type(str): The stat type to get (best-attacks, best-defences, goalscorers, win-ratios)
            Returns:
                table_view(QTableView): Gui-table populated with stats
        """
        # get stats from solr
        stats = {
            'best-attacks': self.stat.get_win_ratios(),
            'best-defences': self.stat.get_best_defences(),
            'goalscorers': self.stat.get_best_attacks(),
            'win-ratios': self.stat.get_win_ratios()
        }[stat_type]

        # model
        model = QStandardItemModel(len(stats), 2)
        for row in xrange(len(stats)):
            key_item = QStandardItem(stats[row][0])
            value_item = QStandardItem('%.2f' % stats[row][1])
            model.setItem(row, 0, key_item)
            model.setItem(row, 1, value_item)

        # view
        table_view = QTableView()
        table_view.setModel(model)

        return table_view

    def run(self):
        self.show()
        app.exec_()

ScoreView().run()
