# encoding: utf-8

import multiprocessing
import time

from pki_services import settings
from utils import cli


def start_ocsp_server():
    ocsp_server_handler = OcspServer()
    ocsp_server_handler.start()
    ocsp_server_handler.join(1)


class OcspServer(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.client_util = cli.CLI()
        self.stop_event = multiprocessing.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        print("OcspServer startup !!")
        while not self.stop_event.is_set():
            command = r'openssl ocsp -index %s -CA %s -rkey %s -rsigner %s -port %s -out %s -text' % \
                      (settings.OCSP_IDX_FILE, settings.CA_CERTS_FILE,
                       settings.CA_KEY_FILE, settings.CA_CERTS_FILE,
                       settings.OCSP_SERVER_PORT, settings.OCSP_OUT_LOG_FILE)

            if command != "":
                try:
                    out, err = self.client_util.call_wait_rtn(command)
                finally:
                    # if "'%s' already exists in Directory Service" % volume_name in out:
                    #     exec_result = True
                    # elif 'Successfully created volume "%s"' % volume_name in out:
                    #     exec_result = True
                    # else:
                    #     exec_result = False
                    print("call returned!")
