
from urllib.parse import urlparse
from handler import Handler
import os
import requests
import yaml

class GatherClusterOperators(Handler):
    def __init__(self):
        Handler.__init__(self,"/gather-extra/artifacts/clusteroperators.json")

    def processUrl(self, url):

        r = requests.get(url)
        clusteroperators = r.json()

        path = 'out/cluster-scoped-resources/config.openshift.io/'
                    
        self.ensurePathExists(path)
        
        outPath = os.path.join(path,"clusteroperators.yaml")

        print("Saving cluster operators yaml ["+outPath+"]")
        with open(outPath, 'wb') as f:
            f.write(bytes(yaml.dump(clusteroperators),"utf-8"))    
        
    def handle(self,url):        
        self.processUrl(url)
