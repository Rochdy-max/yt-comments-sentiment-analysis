from airflow.models import Variable
from cassandra.cluster import Cluster

CASSANDRA_HOST = Variable.get('CASSANDRA_HOST')
CASSANDRA_KEYSPACE = Variable.get('CASSANDRA_KEYSPACE')
FETCHING_INFO_TABLE = Variable.get('FETCHING_INFO_TABLE')

cluster = Cluster([CASSANDRA_HOST])
session = cluster.connect(CASSANDRA_KEYSPACE)

query = 'SELECT video_id, last_fetching_timestamp FROM {}'.format(FETCHING_INFO_TABLE)
rows = session.execute(query)

for item in rows:
    print(item.video_id, item.last_fetching_timestamp)

