# Wade's tournament results application


 version 1.0 05/24/2015

Installation (Zip file contents)
--------------------------------

The checked in Tournament.zip file contains the following files:


(1) tournament.sql - SQL script containing the individual commands needed to create the
    "tournament" database along with it's associated tables as well as a view.  The 
    script can be executed anytime you want/need to recreate the structure.  On execution
    of the script contents, all data will be lost.
    
    Use the command \i tournament.sql to import the whole file into psql once it's initiated.
    You can also just cut and paste the commands into the psql command line to achieve the
    same results.


(2) tournament.py - Python file containing several methods used in the facilitation of a
    basic tournament 'Swiss style' mapping application.  The methods operate independently
    and can actually be "tested" via exectuion of the it's methods in interactive python mode
    after it a file import from the command line.

    ** Note ** An additional method, (playerMatchCombinationUnique), is implemented to
    indicate the existance of a player pairing in the tournyPlayers table.  For this method,
    the win/loss of the pair does not matter.  The primary purpose is to determine if
    they've played before.

(3) tournament_test.py - Python file containing the "test harness" for the tournament match
    application.

    ** Note ** An additional test case is implemented to determine if a given set of players 
    has already played prior to reporting the tourny match results.
_____________________________________________________________________________________________


In order test/run the tournament match application, perform the following steps:

(1) Unzip the contents of the tournanment.zip into the vagrant subdirectory (It's a folder)
(2) Start the GIT Bash application
(3) CD to the fullstack/vagrant directory structure
(4) Type vagrant up <enter> at the command line
(5) Type vagrant ssh <enter> at the command line
(6) CD to the /vagrant/tournament virtural directory 
(7) At the vagrant command line, type "python tournament_test.py"

The results of a successful application execution displays the 9, (there were originally 8),
test cases.



Copyright 2015 Wade Corporation.  All rights reserved.
Wade's Tournament Results Application and its use are subject to a license agreement and are
also subject to copyright, trademark, patent and/or other laws.