FROM python:3.10-slim
EXPOSE 8080
RUN apt-get update --fix-missing && apt-get install -y ffmpeg
ADD ./requirements.txt /
RUN pip install -r /requirements.txt
ARG GATEWAY
ENV GATEWAY=$GATEWAY
ADD . /plugin
ENV PYTHONPATH=$PYTHONPATH:/plugin
WORKDIR /plugin/services
CMD python services.py
