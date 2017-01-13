#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    query1 = """TRUNCATE TABLE Matches;
    """
    conn = connect()
    c = conn.cursor()
    c.execute(query1)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    query = """TRUNCATE TABLE Players, Matches;
    """
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    query = """SELECT COUNT(*) FROM Players;
    """
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchone()
    conn.close()
    return rows[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO Players (name) VALUES (%s);", (name,))
    conn.commit() 
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    
    query1 = """CREATE OR REPLACE VIEW WinCount as
    SELECT Players.id, Players.name, count(Matches.winner) as wins
    FROM Players left join Matches ON Players.id = Matches.winner
    GROUP BY Players.id
    ORDER BY id; """
    
    query2 = """
    CREATE OR REPLACE VIEW LossCount as
    SELECT Players.id, Players.name, count(Matches.loser) as losses
    FROM Players left join Matches ON Players.id = Matches.loser
    GROUP BY Players.id
    ORDER BY id;"""
    
    query3 = """
    SELECT WinCount.id, WinCount.name, WinCount.wins, WinCount.wins + LossCount.losses as Matches
    FROM WinCount join LossCount ON WinCount.id = LossCount.id;
    """
    conn = connect()
    c = conn.cursor()
    c.execute(query1)
    c.execute(query2)
    c.execute(query3)
    rows = c.fetchall()
    conn.commit() 
    conn.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO Matches (winner, loser) VALUES (%s, %s);", (winner, loser))
    conn.commit() 
    conn.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    
    query = """SELECT Players.id, Players.name, Count(Matches.winner) as wins
      FROM Players left join Matches on Players.id = Matches.winner
      GROUP BY Players.id
      ORDER BY wins DESC;"""
    pairings = []
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    numberRows = len(rows)
    i = 0
    while (i < numberRows):
      pairings.append((rows[i][0], rows[i][1], rows[i+1][0], rows[i+1][1]))
      i += 2
      
    conn.close()
    return pairings
    
    


