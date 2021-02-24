from urllib.parse import urlparse	
from handler import Handler	
import os	
import requests	
import yaml	

class GatherPods(Handler):	
    def __init__(self):	
        Handler.__init__(self,"/gather-extra/artifacts/pods.json")	

    namespaces = {	

    }	

    def storePodYamlForNs(self, pod, namespace):	
        nsArray = {	
                'apiVersion': 'v1',	
                'items':[]	
        }	
        if namespace not in self.namespaces:	
            self.namespaces[namespace] = nsArray	
        else:	
            nsArray = self.namespaces[namespace]	
        nsArray['items'].append(pod)	

    def writeCorePodYamls(self):	
        for namespace in self.namespaces:	
            path = 'out/namespaces/'+namespace+'/core/'	
            self.ensurePathExists(path)	
            outPath = os.path.join(path,"pods.yaml")	
            print("Write pods.yaml to 'core' in ["+namespace+"]")	
            with open(outPath, 'wb') as f:	
                f.write(bytes(yaml.dump(self.namespaces[namespace]),"utf-8"))    	


    def processUrl(self, url):	
        r = requests.get(url)	
        pods = r.json()	

        if 'items' not in pods:	
            return	

        for pod in pods['items']:	
            if 'metadata' not in pod:	
                continue	
            metadata = pod['metadata']	
            if ('name' not in metadata) or \
               ('namespace' not in metadata):	
               continue	

            path = 'out/namespaces/'+   \
                    metadata['namespace']+ \
                    '/pods/'+           \
                    metadata['name']+'/'

            if os.path.exists(path) == False:	
                os.makedirs(path)	

            outPath = os.path.join(path,metadata['name']+".yaml")	
            self.storePodYamlForNs(pod,metadata['namespace'])	
            print("Saving pod yaml ["+outPath+"]")	
            with open(outPath, 'wb') as f:	
                f.write(bytes(yaml.dump(pod),"utf-8"))    	

    def handle(self,url):        	
        self.processUrl(url)	

    def complete(self):	
        self.writeCorePodYamls() 