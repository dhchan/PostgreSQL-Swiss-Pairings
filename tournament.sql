-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--vagrant => psql
--\c tournament   #to connect to the tournament database

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

DROP TABLE IF EXISTS Players;
CREATE TABLE Players (
  id serial primary key,
  name text);
  
DROP TABLE IF EXISTS Matches;
CREATE TABLE Matches (
  match_id serial,
  winner int references Players (id),
  loser int references Players (id));
  
  
INSERT INTO Players (name) VALUES ('A');
INSERT INTO Players (name) VALUES ('B');
INSERT INTO Players (name) VALUES ('C');
INSERT INTO Players (name) VALUES ('D');
INSERT INTO Players (name) VALUES ('E');
INSERT INTO Players (name) VALUES ('F');
INSERT INTO Players (name) VALUES ('G');
INSERT INTO Players (name) VALUES ('H');

INSERT INTO Matches (winner, loser) VALUES (1, 2);
INSERT INTO Matches (winner, loser) VALUES (1, 3);
INSERT INTO Matches (winner, loser) VALUES (1, 4);
INSERT INTO Matches (winner, loser) VALUES (1, 5);
INSERT INTO Matches (winner, loser) VALUES (2, 1);


CREATE OR REPLACE VIEW WinCount as
    SELECT Players.id, Players.name, count(Matches.winner) as wins
    FROM Players left join Matches ON Players.id = Matches.winner
    GROUP BY Players.id
    ORDER BY id;
  
CREATE OR REPLACE VIEW LossCount as
    SELECT Players.id, Players.name, count(Matches.loser) as losses
    FROM Players left join Matches ON Players.id = Matches.loser
    GROUP BY Players.id
    ORDER BY id;
    
SELECT WinCount.id, WinCount.name, WinCount.wins, WinCount.wins + LossCount.losses as Matches
    FROM WinCount join LossCount ON WinCount.id = LossCount.id;

SELECT Players.id, Players.name, Count(Matches.winner) as wins
      FROM Players left join Matches on Players.id = Matches.winner
      GROUP BY Players.id
      ORDER BY wins DESC;
    
