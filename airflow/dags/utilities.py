from textblob import TextBlob
from airflow.models import Variable
from confluent_kafka import Producer

def get_kafka_producer(verbose=False):
    """
    Return a well configured Kafka producer for the current app
    """
    # Producer configuration
    producer_settings = {
        "bootstrap.servers" : Variable.get('KAFKA_BOOTSTRAP_SERVER'),
        "security.protocol": "PLAINTEXT"
    }
    # Create producer
    producer = Producer(producer_settings)

    if verbose:
        # Print kafka metadata
        print()
        print("BROKERS LIST:", *(f'{broker_mtd.host}:{broker_mtd.port}' for _, broker_mtd in producer.list_topics().brokers.items()), sep='\n')
        print()
        print("TOPICS LIST:", *(topic_mtd.topic for id, topic_mtd in producer.list_topics().topics.items()), sep='\n')
        print()
    # Return producer
    return producer

def process_comment_resource(resource):
    """
    Process a YouTube comment resource to obtain essential information in a dictionary object

    :param resource: A dict-like object representing a YouTube comment (returned by an API)

    :return: A dictionnary containing essential information
    :rtype: dict
    """
    snippet = resource.get('snippet')
    comment = {
        "id": resource.get('id'),
        "authorDisplayName": snippet.get('authorDisplayName'),
        "authorChannelId": snippet.get('authorChannelId').get('value') if snippet.get('authorChannelId') else None,
        "channelId": snippet.get('channelId'),
        "textDisplay": snippet.get('textDisplay'),
        "sentimentPolarity": TextBlob(snippet.get('textDisplay')).sentiment.polarity,
        "publishedAt": snippet.get('publishedAt'),
        "updatedAt": snippet.get('updatedAt')
    }
    return comment