/opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka_broker:9092 --create --topic $COMMENTS_TOPIC_NAME

echo -ne "\n\n"
echo "Kafka topic \`$COMMENTS_TOPIC_NAME\` created"