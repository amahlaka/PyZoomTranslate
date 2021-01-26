# Zoom captioning api wrapper (and google translate)
# Written (Copy-pasted) by Arttu Mahlakaarto


import requests
import time
import six
from google.cloud import translate_v2 as translate
import html




class cc_api():
    
    def __init__(self):
        self.url="%ZOOM-TOKEN-PLACEHOLDER%&lang=en-US"  # TODO: read from input or from file, too tired to implement tonight.
        self.seq=0
        self.translate_client = translate.Client()
    
    def send_cc(self,cc):
        try:
            req = requests.post(self.url + "&seq=" + str(self.seq),data=cc.encode('utf-8'),headers={"Content-Type": "text/plain"})
        except:
            print("fail")
            time.sleep(0.04)
            try:
                req = requests.post(self.url + "&seq=" + str(self.seq),data=cc.encode('utf-8'),headers={"Content-Type": "text/plain"})
            except:
                return
        print(req.text)

    def confirm(self,cc):
        c1=self.translate_text(cc.encode('utf-8'))+"\n"
        req = requests.post(self.url + "&seq=" + str(self.seq),data=c1.encode('utf-8'),headers={"Content-Type": "text/plain"})
        self.seq+=1
        f = open("seq.tmp", "w")
        f.write(self.seq)
        f.close()

        print(req.text)
        return

    def translate_text(self, text):


        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = self.translate_client.translate(text, target_language="en",source_language="fi")
        print
        return(html.unescape(result["translatedText"]))