class Author:
    def __init__(self, _name, _email):
        self.name = _name
        self.email = _email
        self.commits = []

    def add_commit(self, _commit):
        self.commits.append(_commit)

class Commit:
    def __init__(self, _sha, _timestamp, _project):
        self.sha = _sha
        self.timestamp = _timestamp
        self.project = _project
        self.files = []
        self.methods = []

    def add_method(self, _method):
        self.methods.append(_method)

    def add_file(self, _file):
        self.files.append(_file)

class Method:
    def __init__(self, _name, _api, _amount_total, _amount_inserted, _amount_removed, _frequency_total, _frequency_inserted, _frequency_removed):
        self.name = _name
        self.api = _api
        self.amount_total = _amount_total
        self.amount_inserted = _amount_inserted
        self.amount_removed = _amount_removed
        self.frequency_total = _frequency_total
        self.frequency_inserted = _frequency_inserted
        self.frequency_removed = _frequency_removed