def Commit():
    def __init__(self, key, author, timestamp, method, project, inserted, removed):
        self.key = key
        self.author = author
        self.timestamp = timestamp
        self.method = method
        self.project = project
        self.inserted = inserted
        self.removed = removed

    def abs(self):
        return self.inserted - self.removed

    