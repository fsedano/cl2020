FROM ubuntu:18.04
RUN apt-get update -y && apt-get install -y curl python3 python3-pip vim git nano inetutils-ping telnet ncurses-dev
RUN pip3 install pyOpenSSL flask-restful
WORKDIR /app
#RUN git clone https://github.com/cisco-ie/cisco-gnmi-python.git
ENTRYPOINT [ "/bin/bash", "-c", "sleep 999999" ]
