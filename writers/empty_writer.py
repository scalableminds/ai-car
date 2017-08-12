from writers import Writer

class EmptyWriter(Writer):

    def write(self, data):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        pass
