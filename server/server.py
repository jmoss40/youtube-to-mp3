from pytube import YouTube, Playlist
import re, os, sys, shutil, tempfile, json, subprocess
from tempfile import TemporaryDirectory
from flask import send_from_directory, send_file, make_response
from os.path import exists
from flask_restful import Api, Resource, reqparse

def convertVideo(url, format="MP4"):
  is_playlist = re.search(r"playlist", url)
  output_file = None
  os.chdir('/tmp')
  path = os.getcwd()
  #temp_dir = tempfile.mkdtemp()

  with TemporaryDirectory() as temp_dir:
    os.chdir(temp_dir)
    if is_playlist:
      p = Playlist(url)
      for video in p.videos:
        file = video.streams.filter(only_audio=True).first().download()
        if format.upper() == "MP3":
          name, ext = os.path.splitext(file)
          subprocess.call(['ffmpeg', '-i', file, name+".mp3"])
          os.remove(file)
      output_file = shutil.make_archive("amber-converter-download", 'zip', temp_dir)
      shutil.move(output_file, path)
    else:
      yt = YouTube(url)
      file = yt.streams.filter(only_audio=True).first().download()
      name, ext = os.path.splitext(file)
      
      if format.upper() == "MP3":
        # name, ext = os.path.splitext(file)
        file = name+".mp3"
        subprocess.call(['ffmpeg', '-i', name+ext, file])
      shutil.move(file, path)
      output_file = file

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
      output_file = convertVideo(str(url), str(form))
    except Exception as e:
      print(str(e))
      return {"status": "Failure", "url": url, "file": output_file, "error": str(e)}

    response = make_response(send_from_directory("/tmp", output_file, as_attachment=True))
    response.headers['Content-Disposition'] = "attachment; filename=%s" % output_file
    return response

