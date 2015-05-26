
-- * Connect to vagrant
\c vagrant

-- * Drop the tournament database
drop database if exists tournament;

-- * Recreate the tournament database
create database tournament;

-- * Connect to the tournament database
\c tournament;

-- * Create the tournament player table
create table tournyPlayers (
        id serial primary key,
	sPlrName text );

-- * Create the tournament matches table
create table tournyMatches (
        id serial primary key,
	sWinner integer references tournyPlayers (id),
	sLoser  integer references tournyPlayers (id));

-- * Create a view of total matches played by for
--  each tournament contestent
create view vtournyMatchesPlayed as select
        tournyPlayers.id as tournyPlayerId, 
        count(tournyMatches.id) as totalmatchesplayed 
        from tournyPlayers left join tournyMatches 
        on tournyplayers.id=swinner or 
        tournyplayers.id=sloser group by tournyplayers.id;