from handler import Handler
import requests
import os
import yaml
class GatherClusterVersion(Handler):
    def __init__(self):
        Handler.__init__(self,"gather-extra/artifacts/clusterversion.json")


    def processUrl(self, url):

        r = requests.get(url)
        clusterversions = r.json()

        if 'items' not in clusterversions:
            return
        
        path = 'out/cluster-scoped-resources/config.openshift.io'
                    
        self.ensurePathExists(path)            

        outPath = os.path.join(path,"clusterversions.yaml")
            
        print("Saving clusterversions yaml ["+outPath+"]")
        with open(outPath, 'wb') as f:
            f.write(bytes(yaml.dump(clusterversions),"utf-8"))    

        path = 'out/cluster-scoped-resources/config.openshift.io/clusterversions'
                    
        self.ensurePathExists(path)                             
        outPath = os.path.join(path,"version.yaml")
            
        print("Saving clusterversion yaml ["+outPath+"]")
        with open(outPath, 'wb') as f:
            f.write(bytes(yaml.dump(clusterversions['items'][0]),"utf-8"))    


    def handle(self,url):        
        self.processUrl(url)
        
