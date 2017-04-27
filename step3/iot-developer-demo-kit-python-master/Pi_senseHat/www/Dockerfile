FROM python:3.5.3-alpine
EXPOSE 8000
COPY app.py /app.py
COPY IOTWrapper.py /IOTWrapper.py
COPY sensor.py /sensor.py
WORKDIR /
CMD python3 /app.py