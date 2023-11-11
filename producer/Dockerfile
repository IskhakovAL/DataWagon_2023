FROM flink:1.17.1-scala_2.12-java11

RUN apt update && apt install -y python3 python3-pip && ln -s /usr/bin/python3 /usr/bin/python

RUN python -m pip install apache-flink python-dotenv

RUN curl -o /opt/flink/lib/flink-connector-kafka-1.17.1.jar https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/1.17.1/flink-connector-kafka-1.17.1.jar && \
    curl -o /opt/flink/lib/kafka-clients-3.4.0.jar https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.0/kafka-clients-3.4.0.jar && \
    curl -o /opt/flink/lib/flink-sql-connector-mongodb-1.0.1-1.17.jar https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-mongodb/1.0.1-1.17/flink-sql-connector-mongodb-1.0.1-1.17.jar && \
    curl -o /opt/flink/lib/postgresql-42.6.0.jar https://jdbc.postgresql.org/download/postgresql-42.6.0.jar && \
    curl -o /opt/flink/lib/flink-connector-jdbc-3.1.1-1.17.jar https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.1-1.17/flink-connector-jdbc-3.1.1-1.17.jar