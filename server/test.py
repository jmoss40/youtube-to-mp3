from pytube import YouTube, Playlist
import re, os, sys, shutil, tempfile, json, subprocess

def convertVideo(url, format="MP4"):
  is_playlist = re.search(r"playlist", url)
  
  output_file = None
  path = os.getcwd()
  temp_dir = tempfile.mkdtemp()
  os.chdir(temp_dir)
  
  print("Inside convertVideo: cwd: " + path)

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
    if format.upper() == "MP3":
      name, ext = os.path.splitext(file)
      file = name+".mp3"
      subprocess.call(['ffmpeg', '-i', name+ext, file])
    shutil.move(file, path)
    output_file = file

  os.chdir('../')
  shutil.rmtree(temp_dir)

  #return send_file(output_file, as_attachment=True)

  # print("\n\nOutput file:  " + output_file)
  return output_file


convertVideo(sys.argv[1], sys.argv[2])