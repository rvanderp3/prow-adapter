
from urllib.parse import urlparse
from handler import Handler
import os
import requests
import yaml

class GatherNodes(Handler):
    def __init__(self):
        Handler.__init__(self,"/gather-extra/artifacts/nodes.json")


    def processUrl(self, url):

        r = requests.get(url)
        nodes = r.json()

        if 'items' not in nodes:
            return
        
        for node in nodes['items']:
            if 'metadata' not in node:
                continue
            metadata = node['metadata']
            if ('name' not in metadata):
               continue

            path = 'out/cluster-scoped-resources/core/nodes/'
                    
            if os.path.exists(path) == False:
                os.makedirs(path)
            
            outPath = os.path.join(path,metadata['name']+".yaml")
            
            print("Saving nodes yaml ["+outPath+"]")
            with open(outPath, 'wb') as f:
                f.write(bytes(yaml.dump(node),"utf-8"))    
        
    def handle(self,url):        
        self.processUrl(url)
        
