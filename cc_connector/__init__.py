class ConnectionStatus(object):
    DISCONNECTED = 0
    CONNECTED = 1
    ERROR = 2


class cc_connector_base(object):
    my_id = None
    connection_status = ConnectionStatus.DISCONNECTED
    username = None
    password = None

