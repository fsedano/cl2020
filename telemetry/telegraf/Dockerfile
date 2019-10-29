FROM ubuntu:18.04

RUN apt-get update && apt-get install -y vim wget gnupg iputils-ping influxdb-client less
WORKDIR /app
RUN wget https://dl.influxdata.com/telegraf/releases/telegraf_1.12.4-1_amd64.deb

RUN apt install ./telegraf_1.12.4-1_amd64.deb

ENTRYPOINT [ "/bin/bash", "-c", "sleep 1000000" ]
#ENTRYPOINT ["telegraf", "--debug"]