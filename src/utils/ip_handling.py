import socket

def get_local_network_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:

        return "0.0.0.0"

def find_completely_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))  
    port = s.getsockname()[1]
    s.close()
    return port