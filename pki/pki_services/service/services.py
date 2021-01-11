# encoding: utf-8

import json
import os
import time

from pki_services import settings
from utils import cli
from utils import x509_cert_utils

client_util = cli.CLI()


def get_cert_serial(cert_file_path):

    # todo: 1. 识别文件后缀名，crt, pem, p12

    pass


def generate_certificate(ext_param, validity=365):

    # 证书序列号文件路径
    ca_serial_file_path = os.path.join(settings.CA_CERTS_PATH, 'ca.srl')
    # 处理证书序列号文件，不存在则新建序列号文件
    serial_no = '10101010'

    if os.path.exists(ca_serial_file_path):
        with open(ca_serial_file_path, 'r') as ca_srl_file:
            serial_no_old = ca_srl_file.readline().replace('\n', '').replace('\r', '')
            hex_serial_no = hex(int(serial_no_old, 16) + 1)
            serial_no = hex_serial_no.__str__()[2:]

    # # 写入新 serial_no 内容
    # command_gen_ca_srl = r'echo ' + serial_no + ' > ' + ca_serial_file_path
    # client_util.call_wait_rtn(command_gen_ca_srl)

    curr_crt_folder = os.path.join(settings.SSL_CERTS_PATH, serial_no)
    if os.path.exists(curr_crt_folder):
        os.removedirs(curr_crt_folder)

    os.makedirs(curr_crt_folder)

    # CA 证书文件路径
    ca_cert_file_path = os.path.join(settings.CA_CERTS_PATH, 'ca.pem')
    # CA 密钥文件路径
    ca_key_file_path = os.path.join(settings.CA_CERTS_PATH, 'ca.key')

    # 客户端证书申请文件 req 路径
    client_req_file_path = os.path.join(curr_crt_folder, serial_no + '.req')
    # 客户端密钥文件路径
    client_key_file_path = os.path.join(curr_crt_folder,  serial_no + '_key.key')
    # crt格式 客户端证书文件路径
    client_cert_file_path = os.path.join(curr_crt_folder,  serial_no + '_cert.crt')

    # pem格式 客户端密钥
    client_cert_pem_path = os.path.join(curr_crt_folder, serial_no + '_cert.pem')
    # pem格式 客户端证书
    client_key_pem_path = os.path.join(curr_crt_folder, serial_no + '_key.pem')

    # pkcs12 文件路径
    p12_file_path = os.path.join(curr_crt_folder, serial_no + '.p12')
    # p12 文件密码
    p12_password = settings.P12_PASSWORD

    # extfile 文件路径
    ext_file_path = os.path.join(curr_crt_folder, serial_no + '_v3_ext.cnf')

    print(client_req_file_path)

    # 用户证书：
    # DN:
    # CN: xsfs - user / xxxxx

    # OU: xsfs - group / xxxx
    # 或者
    # OU: xsfs - group / xxxx; xtreemfs - admin
    # 或者：租户管理员
    # OU: xsfs - group / xxxx; xsfs - operator
    # 或者：平台管理员
    # OU: xsfs - group / xxxx; xsfs - admin

    # admin_level 为创建用户权限，1：平台管理员 2-租户管理员，3-普通用户
    admin_level = 3
    if 'admin_level' in ext_param:
        try:
            admin_level = ext_param['admin_level']
        except Exception as ex:
            pass

    print(ext_param)
    print(admin_level)
    # CN: xsfs - user / xxxxx
    uid_name = ""
    if 'uid' in ext_param:
        try:
            uid = ext_param['uid']
            uid_name = "xsfs-user|"+uid
        except Exception as ex:
            pass

    gid = ""
    if 'gid' in ext_param:
        try:
            json_gid_lst = json.loads(ext_param['gid'])
            if type(json_gid_lst) is list and len(json_gid_lst) > 0:
                gid = json_gid_lst[0]
        except Exception as ex:
            pass

    # gid_name 参数：admin_level=1 格式为： xsfs-admin ,admin_level=2 格式为：xsfs-operator , admin_level=3 格式为:xsfs-group/ xxxx
    gid_name = ""
    if admin_level == '1':
        gid_name = "xsfs-admin"
    elif admin_level == '2':
        gid_name = "xsfs-operator"
    else:
        gid_name = "xsfs-group|" + gid

    subject_info = {
        "org_name": "Huoyin",
        "org_unit_name": gid_name,
        "common_name": uid_name
    }

    # 生成 密钥和 req 文件
    command_1 = r'openssl req -new -newkey rsa:2048 -nodes -out %s -keyout %s -subj "/C=CN/ST=BJ/L=BJ/O=%s/OU=%s/CN=%s"' \
                % (client_req_file_path, client_key_file_path,
                   subject_info['org_name'], subject_info['org_unit_name'], subject_info['common_name'])

    __write_file(ext_file_path, __gen_cert_ext_content(ext_param).split(r'\n'))

    # 生成证书文件
    # extfile 内容先写入文件，再读取文件
    # command_2 = r'openssl x509 -CA %s -CAkey %s -CAserial %s -req -in %s ' \
    #             r'-out %s -days %s -extensions v3_req ' \
    #             r'-extfile %s' \
    #             % (ca_key_file_path, ca_cert_file_path, ca_serial_file_path,
    #                client_req_file_path, client_cert_pem_path, validty, ext_file_path)
    command_2 = r'openssl x509 -CA %s -CAkey %s -CAserial %s -req -in %s ' \
                r'-out %s -days %s -extensions v3_req -extfile %s' \
                % (ca_cert_file_path, ca_key_file_path, ca_serial_file_path,
                   client_req_file_path, client_cert_pem_path, validity, ext_file_path)

    # 生成pkcs12格式文件
    command_3 = r'openssl pkcs12 -export -in %s -inkey %s -out %s -name "client_ca" -certfile %s -password pass:%s' % \
                (client_cert_pem_path, client_key_file_path, p12_file_path, ca_cert_file_path, p12_password)

    # 提取 .pem格式 客户端密钥
    command_4 = r'openssl pkcs12 -in %s -nocerts -out %s -passin pass:%s -passout pass:%s' \
                % (p12_file_path, client_key_pem_path, p12_password, p12_password)

    # 提取 .pem格式 客户端证书
    command_5 = r'openssl pkcs12 -in %s -clcerts -nokeys -out %s -passin pass:%s -passout pass:%s' \
                % (p12_file_path, client_cert_file_path, p12_password, p12_password)

    client_util.call_wait_rtn(command_1)
    client_util.call_wait_rtn(command_2)
    time.sleep(1)
    client_util.call_wait_rtn(command_3)
    client_util.call_wait_rtn(command_4)
    client_util.call_wait_rtn(command_5)

    # todo: check file exists

    paths = {
        'client_pem_cert': client_cert_pem_path,
        'client_pem_key': client_key_pem_path,
        'client_key_key': client_key_file_path,
        'client_crt_cert': client_cert_file_path,
        'client_p12': p12_file_path,
        'ca_pem_cert': ca_cert_file_path,
    }

    return int(serial_no, 16), paths


def __write_file(file_path, content_list):
    with open(file_path, 'w+') as file_handler:
        for content in content_list:
            file_handler.writelines(content + "\n")


def __gen_cert_ext_content(ext_param):
    cert_ext_str = ""

    # r"1.2.3.411=ASN1:UTF8String:cert_code:b96f4b06348a4f94b09dedecee3cb9c4\n1.2.3.412=ASN1:UTF8String:machine_code:123456\n1.2.3.413=ASN1:UTF8String:gid:123456"
    header = r"[ req ]\nreq_extensions = v3_req\n\n[ v3_req ]\n"

    start_tag = r'1.2.3.41'
    index = 1

    for key in ext_param.keys():
        ext_value = ''
        if type(ext_param[key]) is int:
            ext_value = ext_param[key].__str__()
        elif type(ext_param[key]) is list or type(ext_param[key]) is dict:
            ext_value = json.dumps(ext_param[key])

        cert_ext_str += start_tag + index.__str__() + "=ASN1:UTF8String:" + key + ":" + ext_value + r'\n'

        index += 1

    return header + cert_ext_str


def revoke_cert_file(cert_serial_no):
    int_serial_no = int(cert_serial_no)
    hex_serial_no = hex(int_serial_no).__str__()[2:]

    # ca.crl 文件路径
    ca_crl_file_path = os.path.join(settings.CA_CERTS_PATH, 'ca.crl')
    # ca.cnf 文件路径
    ca_cnf_file_path = os.path.join(settings.CA_CERTS_PATH, 'ca.cnf')
    # CA 证书文件路径
    ca_cert_file_path = os.path.join(settings.CA_CERTS_PATH, 'ca.pem')
    # CA 密钥文件路径
    ca_key_file_path = os.path.join(settings.CA_CERTS_PATH, 'ca.key')
    # 客户端证书路径
    client_pem_file_path = os.path.join(settings.SSL_CERTS_PATH, hex_serial_no, hex_serial_no + '_cert.pem')

    command_revoke = r'openssl ca -revoke %s -keyfile %s -cert %s -config %s' \
                     % (client_pem_file_path, ca_key_file_path, ca_cert_file_path, ca_cnf_file_path)

    # command_gen_crl = r'openssl ca -config %s -gencrl -out %s' % (ca_cnf_file_path, ca_crl_file_path)

    client_util.call_wait_rtn(command_revoke)
    # time.sleep(0.5)
    # client_util.call_wait_rtn(command_gen_crl)


def verify_cert_file(client_cert_file_path):
    if os.path.join(client_cert_file_path):
        cert_util = x509_cert_utils.X509CertUtils()
        cert_util.load_pem(client_cert_file_path)
        serial_no = cert_util.get_serial_no()
        return verify_cert_serial_no(serial_no.__str__())
    else:
        raise FileNotFoundError("无法找到需要验证的证书文件")


def verify_cert_serial_no(cert_serial_no):
    # 10进制数字字符串改为16进制字符串
    int_serial_no = int(cert_serial_no)
    hex_serial_no_str = hex(int_serial_no).__str__()[2:]

    # # CA 证书文件路径
    # ca_cert_file_path = os.path.join(settings.CA_CERTS_PATH, 'ca.pem')
    # # 客户端证书路径
    # client_pem_file_path = os.path.join(settings.SSL_CERTS_PATH, cert_serial_no, cert_serial_no + '_cert.pem')
    #
    # command_verify = r'openssl ocsp -issuer %s -cert %s -text -url http://%s:%s -VAfile %s' \
    #                  % (ca_cert_file_path, client_pem_file_path,
    #                     settings.OCSP_SERVER, settings.OCSP_SERVER_PORT, ca_cert_file_path)
    #
    # client_util.call_wait_rtn(command_verify)

    if os.path.exists(settings.OCSP_IDX_FILE):
        all_revoked_certs = []
        with open(settings.OCSP_IDX_FILE, 'r') as index_file:
            for line in index_file:
                all_revoked_certs.append(line)

        if len(all_revoked_certs) > 0:
            for revoked_cert in all_revoked_certs:
                if revoked_cert.__contains__(hex_serial_no_str):
                    return False

    return True


if __name__ == '__main__':
    # serial_no = generate_certificate({'uid': '123123123', 'gid': ['123123', '0987654321'],'admin_level': '1',})
    #
    # revoke_cert_file(serial_no)

    # start_ocsp_server()
    #
    # index = 0
    # while index < 10:
    #     print(index)
    #     time.sleep(1)
    #     index += 1
    pass
