from airflow.decorators import task, dag
import requests, json
from confluent_kafka import Producer
from datetime import datetime, timedelta
from airflow.models import Variable

def fetch_ytb_comments_for_video(video_id: str):
    """
    Fetch comments for a specified YouTube video specified by its ID
    
    :param str video_id: A YouTube video ID

    :return: JSON encoded list of the 100 first comments for the provided video
    :rtype: Any
    """
    # API key for Google (YouTube)
    api_key = Variable.get('GOOGLE_API_KEY')
    # URL to get video comments
    url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&part=id,snippet&videoId={video_id}&maxResults=2'

    response = requests.get(url)
    return response.json()

def publish_to_kafka(video_id=None, data=None):
    """
    Send data to Kafka

    :param (Any | None) video_id: A YouTube video ID
    :param (Any | None) data: JSON object containing the list of comments
    """
    # Kafka topic
    kafka_topic = Variable.get('COMMENTS_TOPIC_NAME')
    # Kafka producer configuration
    producer_settings = {
        "bootstrap.servers" : Variable.get('KAFKA_BOOTSTRAP_SERVER'),
        "security.protocol": "PLAINTEXT"
    }
    # Create producer
    producer = Producer(producer_settings)
    # Print kafka metadata
    # print()
    # print("BROKERS LIST:", *(f'{broker_mtd.host}:{broker_mtd.port}' for _, broker_mtd in producer.list_topics().brokers.items()), sep='\n')
    # print()
    # print("TOPICS LIST:", *(topic_mtd.topic for id, topic_mtd in producer.list_topics().topics.items()), sep='\n')
    # print()

    # Callback for Kafka produce
    def log_delivery_status(err, msg):
        """Reports the delivery status of the message to Kafka."""
        if err is not None:
            print('Message delivery failed:', err)
        else:
            print('Message delivered to', msg.topic(), '[Partition: {}]'.format(msg.partition()))
    # Send data
    print("Sending data...")
    producer.produce(
        kafka_topic,
        key=video_id.encode('utf-8'),
        value=json.dumps(data).encode('utf-8'),
        callback=log_delivery_status
    )
    print("Flushing...")
    producer.flush(10)
    print("END")

# Define data streaming DAG
def stream_ytb_comments():
    """
    Fetch comments and stream it to Kafka
    """
    # YouTube video ID list
    videos = [
        '_VB39Jo8mAQ'
    ]

    for video_id in videos:
        # Fetch comments
        comments = fetch_ytb_comments_for_video(video_id)
        # Send comments to kafka
        publish_to_kafka(
            video_id=video_id,
            data=comments
        )

# Start DAG
if __name__ == '__main__':
    stream_ytb_comments()
