FROM ubuntu:18.04
ENV HTTP_PROXY http://proxy.esl.cisco.com:80
ENV HTTPS_PROXY http://proxy.esl.cisco.com:80
ENV http_proxy http://proxy.esl.cisco.com:80
ENV https_proxy http://proxy.esl.cisco.com:80
ENV no_proxy ".cisco.com"
RUN apt-get update -y && apt-get install -y curl python3 python3-pip vim git nano
RUN pip3 install Pyvmomi pyOpenSSL flask-restful
ENTRYPOINT [ "/bin/bash", "-c", "sleep 999999" ]
