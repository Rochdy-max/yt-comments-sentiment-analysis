import requests, json
from confluent_kafka import Producer

class YtbCommentsStreamingAgent:
    """
    An agent for streaming comments from YouTube
    """
    def __init__(self, api_key: str, producer: Producer, kafka_topic: str):
        """
        Set the internal attributes to values of provided parameters

        :param str api_key: An API key to use for accessing YouTube from GoogleAPIs
        :param KafkaProducer producer: Kafka producer object to send data to the broker
        :param str kafka_topic: Topic name where data will be sent
        """
        self.api_key = api_key
        self.producer = producer
        self.kafka_topic = kafka_topic

    def fetch_ytb_comments(self, video_id: str):
        """
        Fetch comments for a specified YouTube video specified by its ID
        
        :param str video_id: A YouTube video ID

        :return: JSON encoded list of the 100 first comments for the provided video
        :rtype: Any
        """
        url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={self.api_key}&part=id,snippet&videoId={video_id}&maxResults=100'

        response = requests.get(url)
        return response.json()

    def produce_to_kafka(self, key=None, value=None):
        """
        Send data to Kafka

        :param (Any | None) key: Specify a key for the data
        :param (Any | None) value: Value of data
        """
        print("Sending data...")
        self.producer.produce(self.kafka_topic, key=key, value=value)
        print("Flushing...")
        self.producer.flush()

    def start(self):
        """
        Fetch comments and stream it to Kafka
        """
        video_id = '_VB39Jo8mAQ'
        # Fetch comments
        comments = self.fetch_ytb_comments(video_id)
        print(json.dumps(comments, indent=4))
        # Send comments to kafka
        self.produce_to_kafka(key = video_id.encode('utf-8'),
                              value = json.dumps(comments).encode('utf-8'))
        print(f'Data sent to Kafka (TOPIC: {self.kafka_topic})')

# Example of usage
if __name__ == '__main__':
    import os

    kafka_topic = os.environ.get('AIRFLOW_VAR_COMMENTS_TOPIC_NAME')
    api_key = os.environ.get('AIRFLOW_VAR_GOOGLE_API_KEY')
    producer = Producer({
        "bootstrap.servers" : os.environ.get('AIRFLOW_VAR_KAFKA_BOOTSTRAP_SERVER')
    })
    agent = YtbCommentsStreamingAgent(api_key, producer, kafka_topic)
    agent.start()