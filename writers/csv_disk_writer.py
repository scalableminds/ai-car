from writers.writer import Writer


class CSVDiskWriter(Writer):
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, "wt")
        return self

    def __exit__(self, type, value, traceback):
        self.file.close()
        del self.file

    def write(self, data):
        self.file.write("%s\n" % ",".join(data))
        self.file.flush()
