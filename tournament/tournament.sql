-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament
CREATE TABLE players
(
    ID SERIAL PRIMARY KEY,
    name VARCHAR(40) NOT NULL
);
CREATE TABLE match
(
    matchID SERIAL PRIMARY KEY,
    winner INT REFERENCES players(ID) ON DELETE CASCADE,
    loser INT REFERENCES players(ID) ON DELETE CASCADE
);
CREATE VIEW getPlayerStandings
AS select p.ID,
          p.name,
         (select count(*) from match where winner  = p.id) "wins",
         (select count(*) from match where p.id in (loser,winner)) "matches"
          from players p 
          order by 3 desc;










