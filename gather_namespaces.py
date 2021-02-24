
from urllib.parse import urlparse
from handler import Handler
import os
import requests
import yaml

class GatherNamespaces(Handler):
    destPath = ""
    def __init__(self):
        Handler.__init__(self,'gather-extra/artifacts/namespaces.json')

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
            name = metadata['name']
            path = 'out/namespaces/'+name
                    
            if os.path.exists(path) == False:
                os.makedirs(path)
            
            outPath = os.path.join(path,name+".yaml")
            
            print("Saving namespace to yaml ["+outPath+"]")
            with open(outPath, 'wb') as f:
                f.write(bytes(yaml.dump(item),"utf-8"))    
        
    def handle(self,url):           
        self.processUrl(url)
