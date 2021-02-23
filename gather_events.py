
from urllib.parse import urlparse
from handler import Handler
import os
import requests
import yaml

class GatherEvents(Handler):
    def __init__(self):
        Handler.__init__(self,"/gather-extra/artifacts/events.json")

    namespaces = {
        
    }

    def storeEventYamlForNs(self, event, namespace):
        nsArray = {
                'apiVersion': 'v1',
                'items':[]
        }
        if namespace not in self.namespaces:
            self.namespaces[namespace] = nsArray
        else:
            nsArray = self.namespaces[namespace]
        nsArray['items'].append(event)

    def writeCoreEventYamls(self):
        for namespace in self.namespaces:
            path = 'out/namespaces/'+namespace+'/core/'
            self.ensurePathExists(path)
            outPath = os.path.join(path,"events.yaml")
            print("Write events.yaml to 'core' in ["+namespace+"]")
            with open(outPath, 'wb') as f:
                f.write(bytes(yaml.dump(self.namespaces[namespace]),"utf-8"))    


    def processUrl(self, url):

        r = requests.get(url)
        events = r.json()

        if 'items' not in events:
            return
        
        for event in events['items']:
            if 'metadata' not in event:
                continue
            metadata = event['metadata']
            if ('name' not in metadata) or \
               ('namespace' not in metadata):
               continue

            self.storeEventYamlForNs(event,metadata['namespace'])
        
    def handle(self,url):        
        self.processUrl(url)
        self.writeCoreEventYamls()
