import socket

def run_heartbeat(port: int = 5556):
    s = socket.socket()
    s.bind(("0.0.0.0", port))
    s.listen(1)
    while True:
        conn, _ = s.accept()
        conn.close()
