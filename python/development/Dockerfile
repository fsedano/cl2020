FROM ubuntu:18.04
RUN apt-get update -y && apt-get install -y curl python3 python3-pip vim git nano inetutils-ping telnet ncurses-dev
COPY data/ /app/
WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/bin/bash", "-c", "sleep 9999999" ]
