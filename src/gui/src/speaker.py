from pythonosc import udp_client

class Speaker:
    def __init__(self, ip: str = "127.0.0.1", port: int = 2):
        self.client = udp_client.SimpleUDPClient(ip, port)

    def next_left(self, event):
        self.client.send_message("/nexttrial", -1)

    def next_right(self, event):
        self.client.send_message("/nexttrial", 1)

    def left_reward(self, event):
        self.client.send_message("/reward", -1)

    def right_reward(self, event):
        self.client.send_message("/reward", 1)

    def repeat_errors(self, event):
        self.client.send_message("/repeat", 0)

    def stop_session(self, event):
        self.client.send_message("/stop", 0)