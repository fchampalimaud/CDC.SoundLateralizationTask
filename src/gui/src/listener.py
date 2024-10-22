from pythonosc import osc_server
from threading import Thread
from pythonosc.dispatcher import Dispatcher

class Listener:
    """
    A class that mediates the messages received via OSC protocol. The OSC server is launched in a new thread.

    Attributes
    ----------
    server : ThreadingOSCUDPServer
        an instance of the OSC server.
    server_thread : Thread
        the thread where the OSC server is launched.
    """

    def __init__(self, messages: dict, ip: str = "127.0.0.1", port: int = 2):

        dispatcher = Dispatcher()
        adresses = list(messages.keys())
        callbacks = list(messages.values())
        # Adds the message adresses and links them to the respective callback functions
        for i in range(len(messages)):
            dispatcher.map(adresses[i], callbacks[i])
        
        # Configures the OSC server
        self.server = osc_server.ThreadingOSCUDPServer(
            (ip, port), dispatcher)

        # Starts the server thread
        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.start()

    def shutdown(self, event):
        """
        Shutdowns the listener instance (shutdowns the OSC server and the Python thread).

        Parameters
        ----------
        event
            event sent by matplotlib.
        """
        self.server.shutdown()
        self.server_thread.join()