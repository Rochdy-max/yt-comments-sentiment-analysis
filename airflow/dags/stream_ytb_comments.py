import os
import requests
import json
from kafka import KafkaProducer

def fetch_ytb_comments(video_id: str):
    """
    Fetch comments for a specified YouTube video
    """
    api_key = os.environ.get('GOOGLE_API_KEY')
    url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&part=id,snippet&videoId={video_id}&maxResults=100'

    response = requests.get(url)
    return response.json()

def produce_to_kafka(producer: KafkaProducer, topic_name: str, key=None, value=None):
    """
    Send data to Kafka
    """
    producer.send(topic_name, key=key, value=value)
    producer.flush()

def stream_ytb_comments():
    """
    Fetch comments and stream it to Kafka
    """
    video_id = '_VB39Jo8mAQ'
    kafka_topic = os.environ.get('COMMENTS_TOPIC_NAME')
    producer = KafkaProducer(bootstrap_servers = [os.environ.get('KAFKA_BOOTSTRAP_SERVER')],
                             api_version = (0,11,5))
    # fetch comments
    comments = fetch_ytb_comments(video_id)
    print(json.dumps(comments, indent=4))
    # send comments to kafka
    produce_to_kafka(producer,
                     kafka_topic,
                     key = video_id.encode('utf-8'),
                     value = json.dumps(comments).encode('utf-8'))
    print(f'Data sent to Kafka (TOPIC: {kafka_topic})')

if __name__ == '__main__':
    stream_ytb_comments()