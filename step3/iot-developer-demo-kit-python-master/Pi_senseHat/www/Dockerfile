FROM alpine:3.5
RUN apk add --update \
 python3
RUN pip3 install flask
RUN pip3 install requests
EXPOSE 8000
COPY app.py /app.py
COPY IOTWrapper.py /IOTWrapper.py
COPY sensor.py /sensor.py
WORKDIR /
CMD python3 /app.py