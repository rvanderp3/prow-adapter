
from urllib.parse import urlparse
from handler import Handler
import os
import requests
import yaml

class GatherResourceToFiles(Handler):
    destPath = ""
    def __init__(self, sourcePath, destPath):
        self.destPath = destPath
        Handler.__init__(self,sourcePath)

    def processUrl(self, url):
        r = requests.get(url)
        itemsObj = r.json()        
        if 'items' not in itemsObj:
            return
        
        for item in itemsObj['items']:
            if 'metadata' not in item:
                continue
            metadata = item['metadata']
            if ('name' not in metadata):
               continue

            path = 'out/'+self.destPath
                    
            if os.path.exists(path) == False:
                os.makedirs(path)
            
            outPath = os.path.join(path,metadata['name']+".yaml")
            
            print("Saving resource to yaml ["+outPath+"]")
            with open(outPath, 'wb') as f:
                f.write(bytes(yaml.dump(item),"utf-8"))    
        
    def handle(self,url):           
        self.processUrl(url)
