
from urllib.parse import urlparse
from handler import Handler
import os
import requests
import yaml
from job_handler import submitJob, tp

class GatherClusterResources(Handler):
    collections = []
    def __init__(self):
         self.collections = [{
            'path': '/gather-extra/artifacts/nodes.json',
            'outputDir': 'core/nodes'            
        },
        {
            'path': 'gather-extra/artifacts/persistentvolumes.json',
            'outputDir': 'core/persistentvolumes'
        },
        {
            'path': 'gather-extra/artifacts/clusterversion.json',
            'outputDir': 'config.openshift.io',
            'outputName': 'clusterversions.yaml'
        },
        {
            'path': 'gather-extra/artifacts/clusteroperators.json',
            'outputDir': 'config.openshift.io',
            'outputName': 'clusteroperators.yaml'
        },
        {
            'path': 'gather-extra/artifacts/clusteroperators.json',
            'outputDir': 'config.openshift.io/clusteroperators',         
        },
        {
            'path': 'gather-extra/artifacts/machineconfigpools.json',
            'outputDir': 'config.openshift.io/machineconfiguration.openshift.io/machineconfigpools',         
        },
        {
            'path': 'gather-extra/artifacts/machineconfigs.json',
            'outputDir': 'config.openshift.io/machineconfiguration.openshift.io/machineconfigs',         
        }]

    def processResource(self, url, collection):
        r = requests.get(url)
        resource = r.json()

        expandInDir = 'outputName' not in collection

        if expandInDir:
            if 'items' not in resource:
                return
            
            for resourceItem in resource['items']:
                if 'metadata' not in resourceItem:
                    continue

                metadata = resourceItem['metadata']
                if ('name' not in metadata):
                    continue

                path = 'out/cluster-scoped-resources/'+collection['outputDir']
                        
                if os.path.exists(path) == False:
                    os.makedirs(path)
                
                outPath = os.path.join(path,metadata['name']+".yaml")
                
                print("Saving yaml ["+outPath+"]")
                with open(outPath, 'wb') as f:
                    f.write(bytes(yaml.dump(resourceItem),"utf-8"))    
        else:
            path = 'out/cluster-scoped-resources/'+collection['outputDir']
                    
            if os.path.exists(path) == False:
                os.makedirs(path)
            
            outPath = os.path.join(path,collection['outputName'])
            
            print("Saving yaml ["+outPath+"]")
            with open(outPath, 'wb') as f:
                f.write(bytes(yaml.dump(resource),"utf-8"))    

    
    def processUrl(self, url):
        for collection in self.collections:
            if collection['path'] in url:
                submitJob(self.processResource,url, collection)

                
    def handle(self,url):        
        self.processUrl(url)        
        
    def handles(self, url):
        for collection in self.collections:            
            if collection['path'] in url:
                return True

