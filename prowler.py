#!/usr/bin/python3
import argparse
import requests
from html.parser import HTMLParser
from urllib.parse import urlparse
from gather_pod_logs import GatherPodLogs
from gather_resources_to_namespaces import GatherResourcesToNamespaces
from gather_finished import GatherFinished
from gather_cluster_resources import GatherClusterResources
from gather_namespaces import GatherNamespaces
from gather_pods import GatherPods
from gather_must_gather import GatherMustGather
from job_handler import waitForJobsToComplete

IGNORE_PATHS = ['artifacts/junit']

BASE_DOMAIN=""
BASE_URL=""

HANDLERS = [
    
]

def handle(url):
    for handler in HANDLERS:
        if handler.enabled() and handler.handles(url):
            handler.handle(url)

class TagParser(HTMLParser):
    startUrl = ""
    def __init__(self, startUrl):
        self.startUrl = startUrl
        HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        if tag == "a":            
            attrs = dict(attrs)            
            if "href" in attrs.keys():
                url = "https://"+BASE_DOMAIN+attrs['href']
                if len(url) <= len(self.startUrl):
                    return                
                
                if url.endswith("/"):
                    getLinksAtLocation(url)
                else:
                    handle(url)

def getLinksAtLocation(url):
    for IGNORE_PATH in IGNORE_PATHS:
        if IGNORE_PATH in url:
            return

    response = requests.get(url)
    parser = TagParser(url)
    parser.feed(response.text)

def buildHandlers(mgOnly):
    HANDLERS.append(GatherFinished())
    
    if mgOnly.lower() == 'true':
        HANDLERS.append(GatherMustGather())        
    else:
        HANDLERS.append(GatherClusterResources())
        HANDLERS.append(GatherPods())
        HANDLERS.append(GatherResourcesToNamespaces())
        HANDLERS.append(GatherNamespaces())
        


parser = argparse.ArgumentParser(description="Translates logs from prow in to something that omg and Insights can analyze")
parser.add_argument('--url', dest='base_url', type=str, help='URL to prow job', required=True)
parser.add_argument('--must-gather', dest='mg_enable', type=str, help='Retrieves a must-gather from the build if it exists.  If false, a must-gather archive is constructed from available data.', default='true')
args = parser.parse_args()

BASE_URL = args.base_url
MG_ENABLE = args.mg_enable
url = urlparse(BASE_URL)

BASE_DOMAIN = url.hostname

buildHandlers(MG_ENABLE)
getLinksAtLocation(BASE_URL)

waitForJobsToComplete()

for handler in HANDLERS:
    handler.complete()


