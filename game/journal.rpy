init python:
    class Journal():
        def __init__(self, entry = []):
            self.entry = []

        def addEntry(self, newEntry):
            self.entry.append(newEntry)
        
        def getEntry(self):
            fullEntry = " ".join(self.entry)
            return fullEntry