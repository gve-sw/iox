FROM alpine:3.5
RUN apk add --update \
 python3
RUN pip3 install bottle
EXPOSE 8000
COPY app.py /app.py
COPY IOTWrapper.py /IOTWrapper.py
COPY sensor.py /sensor.py
COPY static /static
CMD python3 /app.py