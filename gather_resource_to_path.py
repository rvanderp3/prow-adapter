
from urllib.parse import urlparse
from handler import Handler
import os
import requests
import yaml

class GatherResourceToPath(Handler):
    sourcePath = ""
    destPath = ""
    destPathName=""
    def __init__(self, sourcePath, destPath, destPathName):
        self.destPath = destPath
        self.destPathName = destPathName
        Handler.__init__(self,sourcePath)

    def processUrl(self, url):

        r = requests.get(url)
        clusteroperators = r.json()

        #if 'items' in clusteroperators and len(clusteroperators['items']) > 0:
        #    clusteroperators = clusteroperators['items'][0]

        path = 'out/'+self.destPath
                    
        self.ensurePathExists(path)
        
        outPath = os.path.join(path,self.destPathName)

        print("Saving yaml ["+self.destPathName+"]")
        with open(outPath, 'wb') as f:
            f.write(bytes(yaml.dump(clusteroperators),"utf-8"))    
        
    def handle(self,url):
        self.processUrl(url)