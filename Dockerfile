FROM tiangolo/uwsgi-nginx-flask:python3.8

ENV stream1=rtsp://stream.local:3553/234sdflkjsdf \
  stream2=rtsp://stream.local:3553/09823498hsgjhsdg \
  FLASK_APP=streams \
  FLASK_DEBUG=1 \
  STATIC_PATH=/app/static


RUN apt update && apt install -y ffmpeg
COPY ./src /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
