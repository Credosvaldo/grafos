from enum import Enum


class ConnectivityDegree(Enum):
    DISCONNECTED = 0
    WEAKLY_CONNECTED = 1
    UNIDIRECTIONAL_CONNECTED = 2
    STRONGLY_CONNECTED = 3