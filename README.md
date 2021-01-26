# PyZoomTranslate
Python based auto translating captioning tool for Zoom

## How this works:
Zoom sends a livestream of the meeting to a NGINX rtmp endpoint,  
ffmpeg takes the audio from that stream and feeds it to a virtual loopback device.  
The python code then listens to that device, and sends the audio to Google's Cloud Speech to Text api,  
which returns with the text version of your speech, then, that text is send to Google Translate,  
and after being translated, it is sent to the zoom "Live caption" api.

It's a dirty, hacky way to do it 

No Warranty

If I have time to properly document this (and to make it actually stable), I will.  
Feel free to submit pull requests if you want to help :)  

The code is currently translating from Finnish to English (That is easy to change)!  


This early version was made in one single evening, so it's not pretty, but it works (somehow). 


## API's used, documentation:
https://cloud.google.com/speech-to-text/  
https://cloud.google.com/translate  
https://support.zoom.us/hc/en-us/articles/115002212983-Integrating-a-third-party-closed-captioning-service  

## Notes:
 - Open Firewall on port 1935
 - Refresh zoom url
 - start pulseaudio
 - start nginx
 - start ffmpeg
 - Export the api token json filename to env var
 - Start virtual audio devices (Start the speaker first)


## Troubleshooting:
Missing Python.h file when installing dependencies?
``` apt-get install python3.x-dev```

## Pulseaudio and ffmpeg:

 ```sh 
 pactl load-module module-null-sink sink_name="virtual_speaker" sink_properties=device.description="virtual_speaker"
 pactl load-module module-remap-source master="virtual_speaker.monitor" source_name="virtual_mic" source_properties=device.description="virtual_mic"
 ```

Do this after the stream is up and running
 ```sh
ffmpeg -i rtmp://127.0.0.1/live/tv -f pulse "virtual_speaker"
 ```
 



## Zoom configuration:
    Under Advanced meeting settings, enable livestreaming of meetings to custom services and live captioning
    https://us04web.zoom.us/profile/setting

    When you are in the meeting:
    Configure livestream,
    Open "Live captions", select "use 3rd party captioning service, copy apikey to the zoom.py file



## NGINX Configuration


 https://www.nginx.com/blog/video-streaming-for-remote-learning-with-nginx/


 NOTE: THIS CONFIG HAS NO ACCESS CONTROL!!!!!
 DO NOT USE THIS IN A SENSITIVE ENVIROMENT!

 ```apacheconf
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        # multi_accept on;
}
rtmp {
    server {
        listen 1935;
        application live {
            live on;
            interleave on;

            hls on;
            hls_path /tmp/hls;
            hls_fragment 15s;
        }
    }
}

http {
    default_type application/octet-stream;

    server {
        listen 80;
        location /tv {
            root /tmp/hls;
        }
    }

    types {
        application/vnd.apple.mpegurl m3u8;
        video/mp2t ts;
        text/html html;
    }
}
```
