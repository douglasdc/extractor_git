import copy

def get_amount_inserted(_methods):
    return sum(1 for method in _methods if method.amount_inserted > 0)

def get_amount_removed(_methods):
    return sum(1 for method in _methods if method.amount_removed > 0)

def get_frequency_inserted(_methods):
    return sum(method.amount_inserted for method in _methods)

def get_frequency_removed(_methods):
    return sum(method.amount_removed for method in _methods)

class Author:
    def __init__(self, _name, _email):
        self.name = _name
        self.email = _email
        self.commits = {}

    def add_commit(self, _commit):
        if _commit.sha1 in self.commits:
            self.commits[_commit.sha1].add_files(_commit.files)
        else:
            self.commits[_commit.sha1] = _commit

    def get_methods(self):
        methods = {}
        for key, commit in self.commits.items():
            for key, method in commit.get_methods().items():
                if key in methods:
                    methods[method.name].amount_inserted +=  method.amount_inserted
                    methods[method.name].amount_removed +=  method.amount_removed
                else:
                    methods[method.name] = copy.deepcopy(method)
        return methods

class Commit:
    def __init__(self, _sha1, _timestamp, _project):
        self.sha1 = _sha1
        self.timestamp = _timestamp
        self.project = _project
        self.files = []

    def add_file(self, _file):
        self.files.append(_file)

    def add_files(self, _files):
        for f in _files:
            self.files.append(f)

    def get_methods(self):
        methods = {}
        for file in self.files:
            for method in file.methods:
                if method.name in methods:
                    methods[method.name].amount_inserted +=  method.amount_inserted
                    methods[method.name].amount_removed +=  method.amount_removed
                else:
                    methods[method.name] = copy.deepcopy(method)

        return methods


    def __contains__(self, elem):
        return self.sha1 == elem.sha1

class File:
    def __init__(self, _path):
        self.path = _path
        self.methods = set()
    
    def add_method(self, _method):
        self.methods.add(_method)

    def add_methods(self, _methods=[]):
        self.methods = self.methods.union(set(_methods))

    def __contains__(self, elem):
        return self.path == elem.path

class Method:
    def __init__(self, _name, _api, _amount_inserted, _amount_removed, _frequency_inserted, _frequency_removed):
        self.name = _name
        self.api = _api
        self.amount_inserted = _amount_inserted
        self.amount_removed = _amount_removed
        self.frequency_inserted = _frequency_inserted
        self.frequency_removed = _frequency_removed

    def get_frequency(self, removed=True, inserted=True):
        if removed and inserted:
            return self.amount_inserted + self.amount_removed
        elif removed and not inserted:
            return self.amount_removed
        else:
            return self.amount_inserted

    def __contains__(self, elem):
        return self.name == elem.name