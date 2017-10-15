class Author():
    def __init__(self, name, method, inserted, removed):
        self.name = name
        self.inserted = inserted
        self.removed = removed
        
        m = Method(method, inserted, removed)
        self.method = [m]

    def insert_method(self, method, inserted, removed):
        m = Method(method, inserted, removed)
        self.method.append(m)
        return m


class Commit():
    def __init__(self, key, author, timestamp, method, project, inserted, removed):
        self.key = key
        self.author = author
        self.timestamp = timestamp
        self.project = project

        m = Method(method, inserted, removed)
        self.method = [m]

    def insert_method(self, method, inserted, removed):
        m = Method(method, inserted, removed)
        self.method.append(m)
        return m


class Method():
    def __init__(self, name, inserted, removed):
        self.name = name
        self.inserted = inserted
        self.removed = removed

    def abs(self):
        return self.inserted - self.removed
