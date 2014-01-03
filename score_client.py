#!/usr/bin/python

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from stats import ScoreStats


app = QApplication(sys.argv)

class ScoreView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Matchendirect.fr stats')
        self.stat = ScoreStats()
        self.layout = QHBoxLayout()

        # add 'tree' navigation (country > leagues > team)
        self.nav = QHBoxLayout()
        self.nav.addWidget(self.get_tree_view())
        self.nav.addStretch()
        self.layout.addLayout(self.nav)

        # add best stats 'tables' to the grid
        self.grid = QGridLayout()
        self.grid.setSpacing(30)
        self.grid.addWidget(self.get_table_view('best-attacks'), 0, 0)
        self.grid.addWidget(self.get_table_view('best-defences'), 0, 1)
        self.grid.addWidget(self.get_table_view('win-ratios'), 1, 0)
        self.grid.addWidget(self.get_table_view('goalscorers'), 1, 1)
        self.layout.addLayout(self.grid)

        self.setLayout(self.layout)

    def get_tree_view(self):
        """ Returns the tree-navigation view (country > league > team) 

            Returns:
                tree_view(QTableView): countries filters
        """
        # model
        model = QStandardItemModel()
        model.setHorizontalHeaderItem(0, QStandardItem('Countries'))
        root = model.invisibleRootItem()

        # build 'countries' tree
        countries = self.stat.get_countries()
        for country_row in xrange(len(countries)):
            country = countries[country_row][0]
            country_count = countries[country_row][1]
            country_facet_item = QStandardItem('%s (%d)' % (country, country_count))
            root.appendRow(country_facet_item)

            # build 'leagues' tree
            leagues = self.stat.get_leagues(country)
            for league_row in xrange(len(leagues)):
                league = leagues[league_row][0]
                league_count = leagues[league_row][1]
                league_facet_item = QStandardItem('%s (%d)' % (league, league_count))
                country_facet_item.appendRow(league_facet_item)

                # build 'teams' tree
                teams = self.stat.get_teams(country, league)
                for team_row in xrange(len(teams)):
                    team = teams[team_row][0]
                    team_count = teams[team_row][1]
                    team_facet_item = QStandardItem('%s (%d)' % (team, team_count))
                    league_facet_item.appendRow(team_facet_item)

        # view
        tree_view = QTreeView()
        tree_view.setModel(model)

        return tree_view
    
    def get_table_view(self, stat_type):
        """ Returns the table view, of the given stat type

            Args:
                stat_type(str): The stat type to get (best-attacks, best-defences, win-ratios, goalscorers)
            Returns:
                table_view(QTableView): Gui-table populated with stats
        """
        # get stats from solr
        stats = {
            'best-attacks': self.stat.get_best_attacks(),
            'best-defences': self.stat.get_best_defences(),
            'win-ratios': self.stat.get_win_ratios(),
            'goalscorers': self.stat.get_goal_scorers()
        }[stat_type]

        # model
        model = QStandardItemModel(len(stats), 2)
        headers = {
            'best-attacks': ['Team', 'Goals'],
            'best-defences': ['Team', 'Goals'],
            'win-ratios': ['Team', '% of Wins'],
            'goalscorers': ['Player', 'Goals'],
        }[stat_type]
        model.setHorizontalHeaderItem(0, QStandardItem(headers[0]))
        model.setHorizontalHeaderItem(1, QStandardItem(headers[1]))

        for row in xrange(len(stats)):
            key_item = QStandardItem(stats[row][0])
            value_item = QStandardItem('%.2f' % stats[row][1]) if stat_type == 'win-ratios' else QStandardItem('%d' % stats[row][1])  
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
