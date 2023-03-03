FROM python:3.9-slim

COPY --from=openjdk:11-jre-slim /usr/local/openjdk-11 /usr/local/openjdk-11
ENV JAVA_HOME /usr/local/openjdk-11
RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-11/bin/java 1

ADD https://dlcdn.apache.org/maven/maven-3/3.9.0/binaries/apache-maven-3.9.0-bin.tar.gz /tmp/
RUN tar xzvf /tmp/apache-maven-3.9.0-bin.tar.gz --directory=/usr/local/
RUN update-alternatives --install /usr/bin/mvn mvn /usr/local/apache-maven-3.9.0/bin/mvn 1

COPY tests/requirements.txt /usr/local
RUN pip install -r /usr/local/requirements.txt

# Hack to force there to exist a pom.xml file above /tests/ with a node at //root/version
RUN echo "<project><version>NOT_A_VERSION</version></project>" > /pom.xml

# Copy template results index which can be copied for all results
COPY results-index.html /

WORKDIR /tests

# Run with the standard user (1000) instead of root (0) to avoid file permission issues
RUN echo "user:x:1000:1000:user:/home/user:/bin/bash" >> /etc/passwd
RUN mkdir -p /home/user
USER user
