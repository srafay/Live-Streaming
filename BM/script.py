from subprocess import call
import requests
import json
import random
import threading

adsCount = {}
lastfilename = "" 

def matchclip():
    filename = lastfilename
    with open(filename, 'rb') as f:
        r = requests.post('http://ec2-18-217-247-101.us-east-2.compute.amazonaws.com/api/clip/match', files={'uploaded_file': f})
        response = r.json()
        print filename
        print response["found"]
        if response["found"] == "true":
            if response["song_name"] in adsCount:
                adsCount[response["song_name"]] = adsCount[response["song_name"]] + 1
            else:
                adsCount[response["song_name"]] = 1

def parallelmatching():
    matchclip()
    threading.Timer(15.0, parallelmatching).start()

# for i in range(1,4):
delay = threading.Timer(15.0, parallelmatching)
delay.start()

while(1):
    filename = "out{0}.mp4".format(random.randint(1,100))
    lastfilename = filename
    call(["ffmpeg", "-i", "http://streamer64.eboundservices.com/geo/geonews_abr/playlist.m3u8", "-c", "copy", "-bsf:a", "aac_adtstoasc", "-vn", "-t", "15", filename])

# print adsCount

# import httplib, mimetypes

# def post_multipart(host, uri, fields, files):
#     content_type, body = encode_multipart_formdata(fields, files)
#     h = httplib.HTTPConnection(host)
#     headers = {
#         'User-Agent': 'INSERT USERAGENTNAME',
#         'Content-Type': content_type
#         }
#     h.request('POST', uri, body, headers)
#     res = h.getresponse()
#     return res.status, res.reason, res.read() 

# def encode_multipart_formdata(fields, files):
#     """
#     fields is a sequence of (name, value) elements for regular form fields.
#     files is a sequence of (name, filename, value) elements for data to be uploaded as files
#     Return (content_type, body) ready for httplib.HTTP instance
#     """
#     BOUNDARY = '----------bound@ry_$'
#     CRLF = '\r\n'
#     L = []
#     for (key, value) in fields:
#         L.append('--' + BOUNDARY)
#         L.append('Content-Disposition: form-data; name="%s"' % key)
#         L.append('')
#         L.append(value)
#     for (key, filename, value) in files:
#         L.append('--' + BOUNDARY)
#         L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
#         L.append('Content-Type: %s' % get_content_type(filename))
#         L.append('')
#         L.append(value)
#     L.append('--' + BOUNDARY + '--')
#     L.append('')
#     body = CRLF.join(L)
#     content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
#     return content_type, body

# def get_content_type(filename):
#     return mimetypes.guess_type(filename)[0] or 'application/octet-stream'