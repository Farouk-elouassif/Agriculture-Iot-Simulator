FROM eclipse-temurin:17-jre

ARG FLUME_VERSION=1.11.0
ENV FLUME_HOME=/opt/flume
ENV PATH="${FLUME_HOME}/bin:${PATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates tar \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fSL "https://archive.apache.org/dist/flume/${FLUME_VERSION}/apache-flume-${FLUME_VERSION}-bin.tar.gz" -o /tmp/flume.tar.gz \
    && tar -xzf /tmp/flume.tar.gz -C /opt \
    && mv "/opt/apache-flume-${FLUME_VERSION}-bin" "${FLUME_HOME}" \
    && rm /tmp/flume.tar.gz

WORKDIR /opt/flume

CMD ["flume-ng", "agent", "--name", "a1", "--conf", "/opt/flume/conf", "--conf-file", "/opt/flume/conf/sim-taildir.conf", "-Dflume.root.logger=INFO,console"]