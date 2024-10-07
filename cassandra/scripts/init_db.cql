-- Create a keyspace
CREATE KEYSPACE IF NOT EXISTS <CASSANDRA_KEYSPACE> WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };

-- Use keyspace
USE <CASSANDRA_KEYSPACE>;

-- Create a table
CREATE TABLE IF NOT EXISTS <FETCHING_INFO_TABLE> (
video_id text PRIMARY KEY,
last_fetching_timestamp timestamp
);
