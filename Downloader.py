#!/usr/bin/python
import requests, re, json, os, shutil, sys
from urlparse import parse_qs

response = requests.get(sys.argv[1])
# search pattern of the response
# print(response.text)
regex = re.search('"args":({.*?}),', response.text)
# the args is a json format string
match = regex.group(1)
data = json.loads(match)
url_data = data['url_encoded_fmt_stream_map']
# url_data = data['probe_url']
video_url = parse_qs(url_data)['url'][1]
# video_url = url_data
# set up file name
if len(sys.argv)>2:
    to_file_path = '/Users/Benedict/Downloads/' + sys.argv[2]+'.mp4'
else:
    to_file_path = '/Users/Benedict/Downloads/' + data['title']+'.mp4'
# open an empty file
write_to_file = open(to_file_path, 'wb')
# get video content via stream
print('Start Download: ' + data['title'])
video_res = requests.get(video_url, stream=True)
if video_res.status_code != requests.codes.ok:
    print('Invalid Response: ' + str(video_res.status_code))
else:
    # copy video stream
    shutil.copyfileobj(video_res.raw, write_to_file)
    write_to_file.close()
    print('Download Complete ! ')
