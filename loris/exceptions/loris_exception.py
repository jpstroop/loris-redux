class LorisException(Exception):
    # Use for, e.g. out of bounds requests, or when a request utilizes a
    # feature that is not enabled.
    def __init__(self, message, http_status_code):
        self.http_status_code = http_status_code
        self.message = message
