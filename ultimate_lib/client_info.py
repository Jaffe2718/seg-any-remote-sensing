# This file contains the ClientInfo class, which is used to store information about the client

class ClientInfo:
    """
    This class is used to store information about the client.
    """
    client_id: str = ''  # client id in uuid format
    connected_time: float = 0  # the UTC time when the client connected to the server
    is_human: bool = False  # whether the client is a human or not
    force_delay: float = 0.2  # delay in seconds before human check to avoid DDOS
    cached_raster: str = ''  # the name of the cached raster
    cached_mask_raster: str = ''  # the name of the cached mask raster
    preview_raster_png: str = ''  # the name of the preview raster png
    preview_mask_png: str = ''  # the name of the preview mask png

    def __init__(self, cid: str, ctime: float):
        self.client_id = cid
        self.connected_time = ctime
