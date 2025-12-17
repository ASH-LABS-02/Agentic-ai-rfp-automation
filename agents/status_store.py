STATUS_LOG = []

def add_status(msg: str):
    STATUS_LOG.append(msg)

def get_status():
    return STATUS_LOG[-10:]
