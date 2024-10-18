from pythonosc import osc_server
from threading import Thread
from pythonosc.dispatcher import Dispatcher

class Listener:
    def __init__(self, messages: dict, ip: str = "127.0.0.1", port: int = 2):

        dispatcher = Dispatcher()
        adresses = list(messages.keys())
        callbacks = list(messages.values())
        for i in range(len(messages)):
            dispatcher.map(adresses[i], callbacks[i])
        
        self.server = osc_server.ThreadingOSCUDPServer(
            (ip, port), dispatcher)

        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.start()

    def shutdown(self, event):
        self.server.shutdown()
        self.server_thread.join()