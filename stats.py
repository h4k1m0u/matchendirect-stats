#!/usr/bin/python

from sunburnt import SolrInterface

class ScoreStats:
    def __init__(self):
        self.si = SolrInterface('http://localhost:8080/solr')
        self.q = self.si.Q(country='Angleterre') & self.si.Q(league='Premier League')

    def get_win_ratio(self):
        """ Returns win-ratio of each team DESC
            Win-ratio = # of games won / (# of games played as host + # of games played as visitor)

            Returns:
                list of tuples (team, win-rate)
        """
        facets = self.si.query(self.q).field_limit('id')\
            .facet_by('host', limit=20)\
            .facet_by('visitor', limit=20)\
            .facet_by('winner', limit=20, mincount=1)\
            .execute()\
            .facet_counts.facet_fields

        # get host, visitor, winner facets
        hosts_facets = dict(facets['host'])
        visitors_facets = dict(facets['visitor'])
        winners_facets = dict(facets['winner'])

        # percentage of # of games won/team
        win_ratio = []
        for team in winners_facets:
            nb_games_won = float(winners_facets.get(team, 0))
            nb_games_played = float(hosts_facets.get(team, 0) + visitors_facets.get(team, 0))
            win_ratio.append((team, (nb_games_won / nb_games_played) * 100))

        return sorted(win_ratio, key=lambda x: x[1], reverse=True)

    def get_best_attacks(self):
        """ Returns best attacks desc

            Returns:
                list of tuples (team, # of goals)
        """
        # count(host == winner)
        self.si.query().field_limit('scorehost').facet_by('host', limit=20)
        # count(visitor == winner)

    def get_goal_scorers(self):
        """ Returns # of goals scored/player desc

            Returns:
                list of tuples (goalscorer, # of goals)
        """
        # # of occurences, not # of docs
        pass
