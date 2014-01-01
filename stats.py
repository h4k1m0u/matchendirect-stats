#!/usr/bin/python

from sunburnt import SolrInterface

class ScoreStats:
    def __init__(self):
        self.si = SolrInterface('http://localhost:8080/solr')
        self.q = self.si.Q(country='Angleterre') & self.si.Q(league='Premier League')

    def get_win_ratio(self):
        """ Returns win-ratio of each team DESC
            Win-ratio = # of games won / (# of games played as host + # of games played as visitor) * 100

            Returns:
                list of tuples (team, win-rate)
        """
        facets = self.si.query(self.q)\
            .field_limit('id')\
            .facet_by('host', limit=20)\
            .facet_by('visitor', limit=20)\
            .facet_by('winner', limit=20, mincount=1)\
            .paginate(rows=0)\
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
        """ Returns best attacks [# of goals scored DESC]

            Returns:
                list of tuples (team, # of goals scored)
        """
        games = self.si.query(self.q)\
            .field_limit([
                'host', 'visitor',
                'scorehost', 'scorevisitor'
            ])\
            .paginate(rows=1000)\
            .execute()

        goals = {}
        for game in games:
            host = game['host']
            visitor = game['visitor']
            scorehost = game['scorehost']
            scorevisitor = game['scorevisitor']
            
            goals[host] = goals[host] + scorehost if host in goals else scorehost
            goals[visitor] = goals[visitor] + scorevisitor if visitor in goals else scorevisitor

        return sorted(goals.items(), key=lambda x: x[1], reverse=True)

    def get_best_defences(self):
        """ Returns best defences [# of goals conceded ASC]

            Returns:
                list of tuples (team, # of goals conceded)
        """
        games = self.si.query(self.q)\
            .field_limit([
                'host', 'visitor',
                'scorehost', 'scorevisitor'
            ])\
            .paginate(rows=1000)\
            .execute()

        goals = {}
        for game in games:
            host = game['host']
            visitor = game['visitor']
            scorehost = game['scorehost']
            scorevisitor = game['scorevisitor']
            
            goals[host] = goals[host] + scorevisitor if host in goals else scorevisitor
            goals[visitor] = goals[visitor] + scorehost if visitor in goals else scorehost

        return sorted(goals.items(), key=lambda x: x[1])

    def get_goal_scorers(self):
        """ Returns best goalscorers DESC
            Notes: 
                - A player can score multiple times/games(doc) => Cannot use facets  
                - Own goals are not counted

            Returns:
                list of tuples (goalscorer, # of goals scored)
        """
        games = self.si.query(self.q)\
            .field_limit([
                'goalscorershost', 'goalscorersvisitor',
                'goaltimeshost', 'goaltimesvisitor',
                'ogtimeshost', 'ogtimesvisitor'
            ])\
            .paginate(rows=1000)\
            .execute()

        # count # of goals scored/player (og not counted)
        goalscorers = {}
        for game in games:
            goalscorershost = game.get('goalscorershost', ())
            goaltimeshost = game.get('goaltimeshost', ())
            ogtimeshost = game.get('ogtimeshost', ())

            for index, goalscorerhost in enumerate(goalscorershost):
                goaltimehost = goaltimeshost[index]    
                if not goaltimehost in ogtimeshost:
                    goalscorers[goalscorerhost] = goalscorers[goalscorerhost] + 1 if goalscorerhost in goalscorers else 1

            goalscorersvisitor = game.get('goalscorersvisitor', ())
            goaltimesvisitor = game.get('goaltimesvisitor', ())
            ogtimesvisitor = game.get('ogtimesvisitor', ())

            for index, goalscorervisitor in enumerate(goalscorersvisitor):
                goaltimevisitor = goaltimesvisitor[index]    
                if not goaltimevisitor in ogtimesvisitor:
                    goalscorers[goalscorervisitor] = goalscorers[goalscorervisitor] + 1 if goalscorervisitor in goalscorers else 1

        return sorted(goalscorers.items(), key=lambda x: x[1], reverse=True)
