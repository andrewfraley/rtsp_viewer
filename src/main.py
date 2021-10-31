import subprocess
import time
import os
from flask import Flask
from flask import render_template


STREAMS = []
STREAMS_STARTED = []
STATIC_PATH = os.environ.get('STATIC_PATH', '/app/static')

FFMPEG_FLAGS = [
    "-c:v libx264",
    "-sc_threshold 0",
    "-g 25",
    "-rtsp_transport tcp",
    "-preset ultrafast",
    "-hls_time 5",
    "-hls_list_size 5",
    "-start_number 1",

    # Disable audio
    "-an",

    # To enable sound
    "-c:a aac",
    "-b:a 160000",
    "-ac 2"
]

for x in range(100):
    stream = os.environ.get('stream%s' % x)
    if stream:
        STREAMS.append(stream)
if not STREAMS:
    error = 'No streamX ENV variables are set.  Set stream1=rtsp://host.local/123 stream2=rtsp://host.local/123 etc.'
    raise RuntimeError(error)

app = Flask(__name__)


@app.route('/')
def default():
    """ Default / response """
    data = {}
    data['streams'] = STREAMS
    started = start_streams(STREAMS)
    if started:
        time.sleep(10)
    return render_template('streams.html', data=data)


def start_streams(streams):
    """ Start the feeds """
    started = False
    for index, url in enumerate(streams):
        if not os.path.exists('/tmp/stream%d' % index):
            pl_path = "%s/playlist%s.m3u8" % (STATIC_PATH, index)
            flags = ' '.join(FFMPEG_FLAGS)
            command = "ffmpeg -i %s -y %s %s" % (url, flags, pl_path)
            command_list = command.split(' ')
            subprocess.Popen(command_list)
            started = True
            open('/tmp/stream%d' % index, 'a').close()
    return started
