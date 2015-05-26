#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def executeDeleteTxn(sSQL):

    # Connect to the database, perform the delete of the specified
    # table data, commit the transaction, then close the connection.
    myConnection = connect()
    myCursor = myConnection.cursor()
    myCursor.execute(sSQL)
    myConnection.commit()
    myConnection.close()


def playerMatchCombinationUnique(iplayer1, iplayer2):
    """Determine if the match combination of players already exists."""

    # Connect to the database and verify the player "id set" is not
    # already inserted into the tournyMatches table.
    myConnection = connect()
    myCursor = myConnection.cursor()

    sMySqlStatement = "select count(*) from tournyMatches \
    where (swinner=%s and sloser=%s) or (swinner=%s and sloser=%s);"
    myCursor.execute(sMySqlStatement, 
        (iplayer1, iplayer2, iplayer2, iplayer1,))

    results = myCursor.fetchone()
    myConnection.close()

    return results[0]

def deleteMatches():
    """Remove all the match records from the database."""

    # Delete the tournament matches
    sMySqlStatement = "delete from tournyMatches;"

    executeDeleteTxn(sMySqlStatement)


def deletePlayers():
    """Remove all the player records from the database."""

    # Delete the tournament players
    sMySqlStatement = "delete from tournyPlayers;"

    executeDeleteTxn(sMySqlStatement)


def countPlayers():
    """Returns the number of players currently registered."""

    myConnection = connect()
    myCursor = myConnection.cursor()

    # Count the current number of registered players
    sMySqlStatement = "select count(*) from tournyPlayers;"

    myCursor.execute(sMySqlStatement)
    results = myCursor.fetchone()
    myConnection.close()

    return results[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    myConnection = connect()
    myCursor = myConnection.cursor()

    # Insert the user into the database
    sMySqlStatement = "insert into tournyPlayers (sPlrName) values(%s)"

    myCursor.execute(sMySqlStatement, (name,))
    myConnection.commit()
    myConnection.close()


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

    myConnection = connect()
    myCursor = myConnection.cursor()

    # Using the tournyPlayers table as the base, build the SQL using
    # left joins agains the tournyMatches table and the vtournyMatchesPlayed
    # view to build out the player standings result table.
    sMySqlStatement = "select tournyPlayers.id, tournyPlayers.sPlrName, \
    count(swinner) as totalwins, totalmatchesplayed from \
    tournyPlayers left join tournyMatches on tournyPlayers.id=swinner \
    left join vtournyMatchesPlayed on tournyPlayers.id=tournyPlayerid \
    group by tournyPlayers.id, totalmatchesplayed order by totalwins desc;"
    
    myCursor.execute(sMySqlStatement)
    results = myCursor.fetchall()
    myConnection.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
    if playerMatchCombinationUnique(winner, loser)==0:
        myConnection = connect()
        myCursor = myConnection.cursor()
    
        # Insert the player match information into the database
        sMySqlStatement = "insert into tournyMatches (sWinner, sLoser) values (%s, %s)"
    
        myCursor.execute(sMySqlStatement,(winner, loser),)
        myConnection.commit()
        myConnection.close()
    else:
        print "This player match combination already exists!!!"
    

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

    # Get the current player standings
    curResults     = playerStandings()        

    # Initialize variables
    lSwissPairings = []
    lTmpResults    = []
    iCnt           = 0

    # Loop through the player stands and pair
    # them up for the next series of games...
    for row in curResults:
        iCnt = iCnt + 1
        lTmpResults.append(row[0])
        lTmpResults.append(row[1])

        # Build out your pairings list
        # as neeced
        if iCnt==2:
            lSwissPairings.append(lTmpResults)
            lTmpResults = []
            iCnt=0
    
    return lSwissPairings
