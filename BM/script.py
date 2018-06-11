#from subprocess import call
import requests
import json
import random
import threading
import os
import commands

adsCount = {}
clips = []

def matchclip(filename):
    filename = ''.join(filename)
    with open(filename, 'rb') as f:
        print (" Sending {} to the server" .format(filename))
        try:
            r = requests.post('http://lb-89089438.us-east-2.elb.amazonaws.com/api/clip/match', files={'uploaded_file': f})
            if r.status_code == 200:
                print (" {} received response from the server" .format(filename))
                response = r.json()
                print response["found"]
                if response["found"] == "true":
                    if response["song_name"] in adsCount:
                        adsCount[response["song_name"]] = adsCount[response["song_name"]] + 1
                    else:
                        adsCount[response["song_name"]] = 1

                    # For testing out
                    clips.append("{}: {}" .format(response["song_name"], filename))
            else:
                print " Error in server response"
                print r.status_code
                print r.text
        except:
            print ("****************** There was an error getting response from the server ******************")
    try:
        os.rename(filename,"clips/{0}".format(filename))
    except:
        os.mkdir("clips")
        os.rename(filename,"clips/{0}".format(filename))
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print ("Ads Count : {}" .format(adsCount))
    print ("Clips: {}" .format(clips))
    print "************************************"

def getStreamURL(youtubeURL):
    return commands.getstatusoutput('youtube-dl -f 92 -g {}' .format(youtubeURL))[1]


# MAIN PROGRAM STARTS HERE

geoYoutubeStreamURL = "https://www.youtube.com/watch?v=x9isphj0Zc4"
print ("Getting stream URL!")
#streamURL = getStreamURL(geoYoutubeStreamURL)
streamURL = "http://streamer64.eboundservices.com/geo/geonews_abr/playlist.m3u8"
print ("Stream URL updated succesfully!")
clipNumber = 1

while(1):
    filename = "out{0}.m4a".format(clipNumber)
#   streamURL = "http://streamer64.eboundservices.com/geo/geonews_abr/playlist.m3u8"
#   call(["ffmpeg", "-i", "http://streamer64.eboundservices.com/geo/geonews_abr/playlist.m3u8", "-c", "copy", "-bsf:a", "aac_adtstoasc", "-vn", "-t", "15", filename])
    print ("\tRecording started {}" .format(filename))
    os.system("ffmpeg -i {} -c copy -vn -ac 2 -acodec aac -strict -2 -format m4a -t 15 {} -loglevel quiet -b:a 320k" .format(streamURL, filename))
#   call(["ffmpeg", "-i", streamURL, "-c", "copy", "-vn", "-ac", "2", "-acodec", "aac", "-strict", "-2", "-format", "m4a", "-t", "15", filename, "-loglevel", "quiet", "-b:a", "320k"])
    print ("\tRecording complete {}" .format(filename))
    thread = threading.Thread(target=matchclip, args=(filename,))
    thread.daemon = True
    thread.start()
    clipNumber += 1

# ffmpeg -i http://streamer64.eboundservices.com/geo/geonews_abr/playlist.m3u8 -c copy -vn -ac 2 -acodec aac -strict -2 -format m4a -t 15 output.mp4
# https://manifest.googlevideo.com/api/manifest/hls_playlist/id/x9isphj0Zc4.1/itag/91/source/yt_live_broadcast/requiressl/yes/ratebypass/yes/live/1/cmbypass/yes/goi/160/sgoap/gir%3Dyes%3Bitag%3D139/sgovp/gir%3Dyes%3Bitag%3D160/hls_chunk_host/r3---sn-jvooxjuoxu-3ipe.googlevideo.com/gcr/pk/ei/eWYcW-2IHor8owP2lLyIBQ/playlist_type/DVR/initcwndbps/1400/mm/32/mn/sn-jvooxjuoxu-3ipe/ms/lv/mv/m/pl/24/dover/10/manifest_duration/30/playlist_duration/30/keepalive/yes/mt/1528587800/disable_polymer/true/ip/111.88.59.195/ipbits/0/expire/1528609497/sparams/ip,ipbits,expire,id,itag,source,requiressl,ratebypass,live,cmbypass,goi,sgoap,sgovp,hls_chunk_host,gcr,ei,playlist_type,initcwndbps,mm,mn,ms,mv,pl/signature/475F62859E6A1D542ABDDD400ABE81B8F9F5C852.62E4C2A302D058A88743F8F6476F69A978C5DE6D/key/dg_yt0/playlist/index.m3u8
