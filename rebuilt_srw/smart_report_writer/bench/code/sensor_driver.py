class Sensor:
    def __init__(self, port):
        self.port = port
    def read(self):
        return 42
def calibrate(sensor: Sensor):
    data = [sensor.read() for _ in range(10)]
    avg = sum(data)/len(data)
    print(f"Average reading: {avg}")
