import os
import sys
import vlc
import time

#http://streamer64.eboundservices.com/geo/geonews_abr/playlist.m3u8
#http://app.pakistanvision.tv:1935/live/PTVnews/player.m3u8
#http://demo.codesamplez.com/html5/video/sample
clipNumber = sys.argv[1]

filepath = 'http://app.pakistanvision.tv:1935/live/PTVnews/player.m3u8'
movie = os.path.expanduser(filepath)
if 'http://' not in filepath:
    if not os.access(movie, os.R_OK):
        print ( 'Error: %s file is not readable' % movie )
        sys.exit(1)

while(1):
    filename_and_command = "--sout=#transcode{vcodec=none,acodec=mp3,ab=320,channels=2,samplerate=44100}:file{dst=example" + str(clipNumber) + ".mp3}"
#    filename_and_command = "--sout=file/ts:example" + str(clipNumber) + ".mp3"
    instance = vlc.Instance(filename_and_command)
    try:
        media = instance.media_new(movie)
    except NameError:
        print ('NameError: % (%s vs Libvlc %s)' % (sys.exc_info()[1],
                        vlc.__version__, vlc.libvlc_get_version()))
        sys.exit(1)
    player = instance.media_player_new()
    player.set_media(media)
    player.play()
    time.sleep(15)
    exit()
