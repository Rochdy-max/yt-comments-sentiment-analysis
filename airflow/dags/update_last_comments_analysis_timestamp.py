from airflow.models import Variable
from cassandra.cluster import Cluster

CASSANDRA_HOST = Variable.get('CASSANDRA_HOST')
CASSANDRA_KEYSPACE = Variable.get('CASSANDRA_KEYSPACE')
FETCHING_INFO_TABLE = Variable.get('FETCHING_INFO_TABLE')

def update_last_comments_analysis_timestamp(video_id):
    cluster = Cluster([CASSANDRA_HOST])
    session = cluster.connect(CASSANDRA_KEYSPACE)

    update_query = 'UPDATE {table_name} SET last_fetching_timestamp = toTimeStamp(now()) WHERE video_id = \'{video_id}\''.format(
        table_name=FETCHING_INFO_TABLE,
        video_id=video_id
    )
    session.execute(update_query)

    read_query = 'SELECT video_id, last_fetching_timestamp FROM {table_name} WHERE video_id = \'{video_id}\''.format(
        table_name=FETCHING_INFO_TABLE,
        video_id=video_id
    )
    rows = session.execute(read_query)

    for item in rows:
        print(item.video_id, item.last_fetching_timestamp)

