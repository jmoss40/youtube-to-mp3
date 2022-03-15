import os
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory
from flask import send_from_directory, make_response
from flask_restful import Resource, reqparse
from pytube import YouTube, Playlist


def convert_video(url, _format="MP4"):
    is_playlist = re.search(r"playlist", url)
    output_file = None
    os.chdir('/tmp')
    path = os.getcwd()
    with TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        if is_playlist:
            p = Playlist(url)
            for video in p.videos:
                _file = video.streams.filter(only_audio=True).first().download()
                if _format.upper() == "MP3":
                    name, ext = os.path.splitext(_file)
                    subprocess.call(['ffmpeg', '-i', _file, name + ".mp3"])
                    os.remove(_file)
            output_file = shutil.make_archive("amber-converter-download", 'zip', temp_dir)
            shutil.move(output_file, path)
        else:
            yt = YouTube(url)
            _file = yt.streams.filter(only_audio=True).first().download()
            name, ext = os.path.splitext(_file)

            if _format.upper() == "MP3":
                # name, ext = os.path.splitext(file)
                _file = name + ".mp3"
                subprocess.call(['ffmpeg', '-i', name + ext, _file])
            shutil.move(_file, path)
            output_file = _file

        os.chdir('../')

    output_file = re.split('^(\/tmp\/tmp[\S]{8}\/)', output_file)[2]
    return output_file


class Server(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str)
        parser.add_argument('url', type=str)

        args = parser.parse_args()
        form = args['type']
        url = args['url']
        output_file = None

        try:
            output_file = convert_video(str(url), str(form))
        except Exception as e:
            print(str(e))
            return {"status": "Failure", "url": url, "file": output_file, "error": str(e)}

        response = make_response(send_from_directory("/tmp", output_file, as_attachment=True))
        response.headers['Content-Disposition'] = "attachment; filename=%s" % output_file
        return response
