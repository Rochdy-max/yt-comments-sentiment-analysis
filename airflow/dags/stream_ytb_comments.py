import requests, json
from airflow.models import Variable
from utilities import get_kafka_producer, process_comment_resource

# API key for Google (YouTube)
API_KEY = Variable.get('GOOGLE_API_KEY')

def fetch_ytb_comments_replies(comment_id: str):
    """
    Fetch all replies to a specific comment identified by its ID

    :param str comment_id: Unique ID of a YouTube comment

    :return: An iterator to a list of all replies to the specified comment
    """
    MAX_RESULTS = 100
    page_token = None

    while True:
        # URL to get replies
        url = f'https://www.googleapis.com/youtube/v3/comments?key={API_KEY}&part=id,snippet&parentId={comment_id}&maxResults={MAX_RESULTS}&textFormat=plainText'
        if page_token:
            url = f'{url}&pageToken={page_token}'
        # Send request
        response = requests.get(url).json()

        items = response.get('items')
        for comment_resource in items:
            yield process_comment_resource(comment_resource)

        page_token = response.get('nextPageToken')
        if not page_token:
            break

def fetch_ytb_comments_for_video(video_id: str):
    """
    Fetch comments for a specified YouTube video specified by its ID
    
    :param str video_id: A YouTube video ID

    :return: An iterator to a list of all comments for the specified video
    """
    MAX_RESULTS = 100
    page_token = None

    while True:
        # URL to get video comments
        url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={API_KEY}&part=id,snippet&videoId={video_id}&maxResults={MAX_RESULTS}&textFormat=plainText'
        if page_token:
            url = f'{url}&pageToken={page_token}'
        # Send request
        response = requests.get(url).json()

        items = response.get('items')
        for comment_thread in items:
            top_comment_resource = comment_thread['snippet']['topLevelComment']
            yield process_comment_resource(top_comment_resource)

            if comment_thread['snippet']['totalReplyCount'] > 0:
                all_replies = fetch_ytb_comments_replies(top_comment_resource.get('id'))
                for comment in all_replies:
                    yield comment

        page_token = response.get('nextPageToken')
        if not page_token:
            break

# Callback for Kafka produce
def log_delivery_status(err, msg):
    """Reports the delivery status of the message to Kafka."""
    if err is not None:
        print('Message delivery failed:', err)
    else:
        pass
        # print('Message delivered to', msg.topic(), '[Partition: {}]'.format(msg.partition()))

def stream_ytb_comments():
    """
    Fetch comments and stream it to Kafka
    """
    # YouTube video ID list
    videos = [
        '_VB39Jo8mAQ'
    ]
    # Kafka topic
    kafka_topic = Variable.get('COMMENTS_TOPIC_NAME')
    # Kafka producer
    producer = get_kafka_producer()

    print('START of streaming')
    for video_id in videos:
        print()
        print(f'Video ID: {video_id}')
        # Fetch comments
        comments = fetch_ytb_comments_for_video(video_id)
        count = 0
        # Send comments to kafka
        for comment in comments:
            comment['videoId'] = video_id
            # Send data
            producer.produce(
                kafka_topic,
                value=json.dumps(comment).encode('utf-8'),
                callback=log_delivery_status
            )
            producer.flush(10)
            count += 1
        print(f'Comments count: {count}')
    print()
    print('END of streaming')

# Start DAG
if __name__ == '__main__':
    stream_ytb_comments()
