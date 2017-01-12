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
  name text,
  wins int,
  matches int);
  
DROP TABLE IF EXISTS Matches;
CREATE TABLE Matches (
  match_id serial,
  player1 int references Players (id),
  player2 int references Players (id),
  winner text);
  
  
INSERT INTO Players (name, wins, matches) VALUES ('A', 3, 3);
INSERT INTO Players (name, wins, matches) VALUES ('B', 2, 3);
INSERT INTO Players (name, wins, matches) VALUES ('C', 1, 3);
INSERT INTO Players (name, wins, matches) VALUES ('D', 0, 3);
INSERT INTO Players (name, wins, matches) VALUES ('E', 3, 3);
INSERT INTO Players (name, wins, matches) VALUES ('F', 0, 3);
INSERT INTO Players (name, wins, matches) VALUES ('G', 1, 3);
INSERT INTO Players (name, wins, matches) VALUES ('H', 2, 3);

SELECT COUNT (*) from Players;

SELECT id, name FROM Players ORDER BY wins DESC LIMIT 2 OFFSET 0;

SELECT id, name FROM Players ORDER BY wins DESC LIMIT 2 OFFSET 2;

SELECT id, name FROM Players ORDER BY wins DESC LIMIT 2 OFFSET 4;

SELECT id, name FROM Players ORDER BY wins DESC LIMIT 2 OFFSET 6;
