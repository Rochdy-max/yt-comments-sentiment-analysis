from airflow.models import Variable
from confluent_kafka import Producer
from stream_ytb_comments import YtbCommentsStreamingAgent

KAFKA_TOPIC = Variable.get('COMMENTS_TOPIC_NAME')

API_KEY = Variable.get('GOOGLE_API_KEY')

def setup_streaming_agent():
    """
    Provide an agent with appropriate configuration for the current app
    """
    # Kafka producer configuration
    producer_settings = {
        "bootstrap.servers" : Variable.get('KAFKA_BOOTSTRAP_SERVER')
    }
    # Create producer
    producer = Producer(producer_settings)
    return YtbCommentsStreamingAgent(API_KEY, producer, KAFKA_TOPIC)
