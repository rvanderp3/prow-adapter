
from urllib.parse import urlparse
from handler import Handler
import os
import requests
import yaml

class GatherClusterOperators(Handler):
    def __init__(self):
        Handler.__init__(self,"/gather-extra/artifacts/clusteroperators.json")

    def outputOperatorYamls(self,clusteroperators):
        path = 'out/cluster-scoped-resources/config.openshift.io/clusteroperators'
        self.ensurePathExists(path)
        if 'items' not in clusteroperators:
            return
        for operator in clusteroperators['items']:
            if 'metadata' not in operator:
                continue
            metadata = operator["metadata"]
            if 'name' not in metadata:
                continue

            outPath = os.path.join(path,metadata["name"]+".yaml")

            print("Saving operator yaml ["+outPath+"]")
            with open(outPath, 'wb') as f:
                f.write(bytes(yaml.dump(operator),"utf-8"))    


    def processUrl(self, url):

        r = requests.get(url)
        clusteroperators = r.json()

        path = 'out/cluster-scoped-resources/config.openshift.io/'
                    
        self.ensurePathExists(path)
        
        outPath = os.path.join(path,"clusteroperators.yaml")

        print("Saving cluster operators yaml ["+outPath+"]")
        with open(outPath, 'wb') as f:
            f.write(bytes(yaml.dump(clusteroperators),"utf-8"))    
        
        self.outputOperatorYamls(clusteroperators)
        
    def handle(self,url):        
        self.processUrl(url)
