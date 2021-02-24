
from urllib.parse import urlparse
from handler import Handler
import os
import requests
import yaml

class GatherMustGather(Handler):
    destPath = ""
    def __init__(self):
        Handler.__init__(self,'gather-must-gather/artifacts/must-gather.tar')

    def processUrl(self, url):
        with requests.get(url) as mg:
            print("Saving must-gather")
            mg.raise_for_status()
            with open("must-gather.tar", 'wb') as f:
                for chunk in mg.iter_content(chunk_size=8192): 
                    print(".", end='', flush=True)
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    f.write(chunk)
                print('Done')
        
    def handle(self,url):           
        self.processUrl(url)
