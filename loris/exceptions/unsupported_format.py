class UnsupportedFormat(Exception):
    def __init__(self, message, http_status_code=404):
        self.http_status_code = http_status_code
        self.message = message
    def __str__(self):
        return repr(self.message)
