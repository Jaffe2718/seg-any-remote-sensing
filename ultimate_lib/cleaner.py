import os
import threading
import time

from ultimate_lib import client_info


class CleanerThread(threading.Thread):
    def __init__(self,
                 path: str,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clean_path = path

    def run(self):
        while True:
            try:
                time.sleep(3600)
                # check all file in the path `self.clean_path`
                for root, dirs, files in os.walk(self.clean_path):
                    for file in files:
                        # if the file is older than 1 day, delete it
                        if time.time() - os.path.getctime(os.path.join(root, file)) > 86400:
                            os.remove(os.path.join(root, file))
                for root, dirs, files in os.walk(self.clean_path):
                    for dir_ in dirs:
                        # if the dir is empty, delete it
                        if not os.listdir(os.path.join(root, dir_)):
                            os.rmdir(os.path.join(root, dir_))
            except:
                pass


class CleanClientThread(threading.Thread):

    """
    This thread is used to clean the clients:
    - when a client is older than 7 days, delete it.
    - when a client is older than 1 hour and not a human, delete it.
    """

    clients: dict[str, client_info.ClientInfo] = {}

    def __init__(self,
                 clients: dict[str, client_info.ClientInfo],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clients = clients

    def run(self):
        while True:
            try:
                time.sleep(3600)
                # iterate all keys in the dict `self.clients`
                for key in self.clients.keys():
                    # if the client is older than 7 days, delete it
                    if time.time() - self.clients[key].connected_time > 604800:
                        del self.clients[key]
            except:
                pass
