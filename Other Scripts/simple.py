import time
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

print ("Recording video...")
response = urlopen("http://demo.codesamplez.com/html5/video/sample")
print ("Response is : " + str(response))
filename = time.strftime("%Y%m%d%H%M%S",time.localtime())+".mp4"
f = open(filename, 'wb')

video_file_size_start = 0  
video_file_size_end = 1048576 * 7  # end in 7 mb 
block_size = 1024

while True:
    try:
        buffer = response.read(block_size)
        print ("Buffer is " + str(buffer))
        video_file_size_start += len(buffer)
        if video_file_size_start > video_file_size_end:
            break
        f.write(buffer)

    except Exception:
        print("")
f.close()
