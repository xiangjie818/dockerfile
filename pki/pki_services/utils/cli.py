# encoding: utf-8

import subprocess
from threading import Timer


class CLI:
    """
    Just a wrapper around the openssl command
    """

    def __init__(self):
        pass

    @staticmethod
    def call_wait_rtn(command, timeout_sec=0):
        print('Running command: %s' % command)
        p = subprocess.Popen(command,
                             stdin=subprocess.DEVNULL,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True,
                             universal_newlines=True)

        timer = None
        if timeout_sec > 0:
            timer = Timer(timeout_sec, p.kill)
            timer.start()

        try:
            out, err = p.communicate()
        finally:
            if timer is not None:
                timer.cancel()

        print("执行输出: " + out.__str__())
        print("错误输出: " + err.__str__())
        print("")
        print("")

        return out, err

    @staticmethod
    def call_async(command):
        print('Async running command: %s' % command)


class CLIError (Exception):
    pass
