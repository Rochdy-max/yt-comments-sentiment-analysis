import os
from kafka import KafkaProducer
from stream_ytb_comments import YtbCommentsStreamingAgent

KAFKA_TOPIC = os.environ.get('COMMENTS_TOPIC_NAME')

API_KEY = os.environ.get('GOOGLE_API_KEY')

def setup_streaming_agent():
    """
    Provide an agent with appropriate configuration for the current app
    """
    # Create producer
    producer = KafkaProducer(
        bootstrap_servers = [os.environ.get('KAFKA_BOOTSTRAP_SERVER')],
        api_version = (0,11,5)
    )
    return YtbCommentsStreamingAgent(API_KEY, producer, KAFKA_TOPIC)
