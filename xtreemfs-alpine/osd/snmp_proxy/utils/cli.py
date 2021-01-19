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

        # print("执行输出: " + out.__str__())
        # print("错误输出: " + err.__str__())
        # print("")
        # print("")

        return out, err

    @staticmethod
    def call_async(command):
        print('Async running command: %s' % command)


class CLIError (Exception):
    pass


# if __name__ == '__main__':
#     cmd = "xtfsutil /opt/xsfs/d3ae5b2f-aafa-4e7e-bb57-78b9f81929f3"
#     out, err = CLI.call_wait_rtn(cmd)
#
#     ret_list = out.split('\n')
#
#     osd_list = []
#     osd_list_start_ln_no = 1
#     line_no = 1
#     for line in ret_list:
#         if "Selectable OSDs" in line:
#             osd_list_start_ln_no = line_no
#
#         if line_no >= osd_list_start_ln_no > 1:
#             line = line.replace("Selectable OSDs", "").strip()
#             osd_list.append(line)
#
#         line_no += 1
#
#     print(osd_list)
