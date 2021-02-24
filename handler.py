import os
class Handler:    
    
    def __init__(self, path):
        self.path = path
        self.enable = True

    def handle(self,url):
        print("Implement me")

    def handles(self, url):
        return self.path in url

    def ensurePathExists(self, path):
        if os.path.exists(path) == False:
            os.makedirs(path)

    def complete(self):
        pass

    def setEnable(self, enable):
        self.enable = enable

    def enabled(self):
        return self.enable

    def getName(self):
        return "---"
        