-- Use keyspace
USE <CASSANDRA_KEYSPACE>;

-- Insert some data
INSERT INTO <FETCHING_INFO_TABLE>
(video_id, last_fetching_timestamp)
VALUES ('9876', toTimeStamp(now()));

INSERT INTO <FETCHING_INFO_TABLE>
(video_id, last_fetching_timestamp)
VALUES ('1234', toTimeStamp(now()));

INSERT INTO <FETCHING_INFO_TABLE>
(video_id, last_fetching_timestamp)
VALUES ('5861', toTimeStamp(now()));
