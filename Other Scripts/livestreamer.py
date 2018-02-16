import livestreamer
streams = livestreamer.streams("http://demo.codesamplez.com/html5/video/sample")
stream = streams["source"]
fd = stream.open()
data = fd.read(1024)
fd.close()
