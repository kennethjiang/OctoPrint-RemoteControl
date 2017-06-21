import json
import octoprint_client

from subprocess import check_output
ip_addresses = check_output(['hostname', '--all-ip-addresses']).split()

def listen_to_octoprint(settings, q):
    def on_connect(ws):
        print(">>> Connected!")

    def on_close(ws):
        print(">>> Oh No! Connection closed! What happened?")

    def on_error(ws, error):
        print("!!! Error: {}".format(error))

    def on_heartbeat(ws):
        q.put(json.dumps({'hb': {'ips': ip_addresses}}))

    def on_message(ws, message_type, message_payload):
        def __deplete_queue__(q):
            while q.qsize() > 10:
                q.get_nowait()

        __deplete_queue__(q)
        q.put(json.dumps(message_payload))

    octoprint_client.init_client(settings)
    socket = octoprint_client.connect_socket(on_connect=on_connect,
                                             on_close=on_close,
                                             on_error=on_error,
                                             on_heartbeat=on_heartbeat,
                                             on_message=on_message)
