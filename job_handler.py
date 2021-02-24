from concurrent.futures import ThreadPoolExecutor
import concurrent

tp = ThreadPoolExecutor(max_workers=20)
futures = []

def submitJob(*argv):
    futures.append(tp.submit(*argv))
    
def waitForJobsToComplete():
    for executor in concurrent.futures.as_completed(futures):
        pass