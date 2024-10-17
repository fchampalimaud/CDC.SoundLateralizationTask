import matplotlib.pyplot as plt
import numpy as np
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import argparse
import time

def main():
    print("Hello from slt-ui!")


def client():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=1,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    for x in range(10):
        client.send_message("/commands", "hello")
        print(x)
        time.sleep(1)


def print_compute_handler(unused_addr, args, volume):
    try:
        print("[{0}] ~ {1}".format(args[0], args[1](volume)))
    except ValueError: pass

def print_volume_handler(unused_addr, args, volume):
    print("[{0}] ~ {1}".format(args[0], volume))

def server():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
        type=int, default=2, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/plots", print)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()



if __name__ == "__main__":
    main()
    client()
    server()
