#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""

    query1 = """TRUNCATE TABLE Matches;
    """
    conn, c = connect()
    c.execute(query1)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    query = """TRUNCATE TABLE Players CASCADE;
    """
    conn, c = connect()
    c.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    query = """SELECT COUNT(*) FROM Players;
    """
    conn, c = connect()
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
    conn, c = connect()
    query = "INSERT INTO Players (name) VALUES (%s);"
    c.execute(query, (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in 1st place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = """SELECT Q1.id, Q1.name, Q1.wins, wins + losses as matches FROM
    (SELECT Players.id, Players.name, count(Matches.winner) as wins
    FROM Players left join Matches ON Players.id = Matches.winner
    GROUP BY Players.id
    ORDER BY Players.id) as Q1,
    (SELECT Players.id, Players.name, count(Matches.loser) as losses
    FROM Players left join Matches ON Players.id = Matches.loser
    GROUP BY Players.id
    ORDER BY Players.id) AS Q2
    WHERE Q1.id = Q2.id;
    """
    conn, c = connect()
    c.execute(query)
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
    conn, c = connect()
    c.execute("INSERT INTO Matches (winner, loser) \
    VALUES (%s, %s);", (winner, loser))
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
    conn, c = connect()
    c.execute(query)
    rows = c.fetchall()
    numberRows = len(rows)
    i = 0
    while (i < numberRows):
        pairings.append((rows[i][0], rows[i][1], rows[i+1][0], rows[i+1][1]))
        i += 2
    conn.close()
    return pairings
