# encoding: utf-8

import json
import os
import time
import tornado.web
import tornado.ioloop
from utils.cli import CLI


# OSDCONFIG_PATH = "/etc/xos/xtreemfs/osdconfig.properties"
OSDCONFIG_PATH = "/etc/xos/xtreemfs/proxy.conf"
ACL_PORT_CFG_NAME = "acl.port"
# 配置文件读取尝试次数
CONFIG_READ_RETRY = 3
CONFIG_READ_RETRY_INTEVAL = 3 
SNMP_PORT = 34640
HOST = "127.0.0.1"


class GetOsdStatusHandler(tornado.web.RequestHandler):
    def get(self):
        print("GetOsdStatusHandler  !!")

        osd_status_mib = "1.3.6.1.4.1.38350.1.11.0"
        snmp_cmd = "snmpget -v2c -cpublic " + HOST + ":" + str(SNMP_PORT) + " " + osd_status_mib

        out, err = CLI.call_wait_rtn(snmp_cmd)

        self.write(json.dumps({
            "out": out,
            "err": err
        }))


class GetConnNumberHandler(tornado.web.RequestHandler):
    def get(self):
        print("GetConnNumberHandler  !!")

        conn_num_mib = "1.3.6.1.4.1.38350.1.8.0"
        snmp_cmd = "snmpget -v2c -cpublic " + HOST + ":" + str(SNMP_PORT) + " " + conn_num_mib

        out, err = CLI.call_wait_rtn(snmp_cmd)

        self.write(json.dumps({
            "out": out,
            "err": err
        }))

def __get_proxy_port():
    retry= 0
    acl_port = None
    while retry < CONFIG_READ_RETRY:
        acl_port = __read_acl_port(OSDCONFIG_PATH)
        if acl_port is not None:
            break

        time.sleep(CONFIG_READ_RETRY_INTEVAL)
        retry += 1

    if retry >= CONFIG_READ_RETRY:
        print("指定位置 " + OSDCONFIG_PATH + " 未读取到配置文件 osdconfig.properties")

    return acl_port
        
def __read_acl_port(cfg_file_path):
    acl_port = None
    if os.path.exists(cfg_file_path):
        with open(cfg_file_path, 'rb') as conf_file:
            print(" ++++++++++++++++++ ")
            for line in conf_file:
                str_line = line.decode('utf-8')
                print(str_line)

                if str_line.startswith(ACL_PORT_CFG_NAME) or \
                    str_line.startswith("#" + ACL_PORT_CFG_NAME) or \
                    str_line.startswith("# " + ACL_PORT_CFG_NAME):

                    acl_ports = str_line.split("=")
                    if len(acl_ports) > 1:
                        acl_port = acl_ports[1].strip()
                        break
            print(" ++++++++++++++++++ ")

    return int(acl_port)


if __name__ == "__main__":
    settings = {
        'debug' : True,
        'static_path' : os.path.join(os.path.dirname(__file__) , "static") ,
        'template_path' : os.path.join(os.path.dirname(__file__) , "template") ,
    }

    application = tornado.web.Application([
        (r"/get_osd_status" , GetOsdStatusHandler),
        (r"/get_conn_number" , GetConnNumberHandler),


    ] , **settings)
    acl_port = __get_proxy_port()
    print("Start snmp proxy with port " + str(acl_port))

    application.listen(acl_port)
    tornado.ioloop.IOLoop.instance().start()