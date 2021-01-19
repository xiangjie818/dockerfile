# encoding: utf-8

import os
from datetime import datetime
from OpenSSL import crypto


class X509CertUtils:
    def __init__(self):
        self.p12_file_path = None
        self.p12_pwd = None
        self.p12 = None
        self.pem_file_path = None
        self.crt_file_path = None
        self.cert = None

    def load_crt(self, crt_file_path):
        if crt_file_path is not None and os.path.exists(crt_file_path):
            self.crt_file_path = crt_file_path
            self.cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(crt_file_path, 'rb').read())
        else:
            raise ValueError("请指定crt证书文件，或确认文件在指定位置")

    def load_pem(self, pem_file_path):
        if pem_file_path is not None and os.path.exists(pem_file_path):
            self.pem_file_path = pem_file_path
            self.cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(pem_file_path, 'rb').read())

        else:
            raise ValueError("请指定pem证书文件，或确认文件在指定位置")

    def load_p12(self, p12_file_path, p12_pwd):
        if p12_file_path is not None and os.path.exists(p12_file_path):
            self.p12_file_path = p12_file_path
            self.p12_pwd = p12_pwd

            self.p12 = crypto.load_pkcs12(open(p12_file_path, 'rb').read(), p12_pwd)
            self.cert = self.p12.get_certificate()
        else:
            raise ValueError("请指定p12证书文件，或确认文件在指定位置")

    def get_serial_no(self):
        return self.cert.get_serial_number()

    def get_all_extensions(self):
        ret_obj = {}
        if self.cert is not None and self.cert.get_extension_count() > 0:
            for i in range(0, self.cert.get_extension_count()):
                item_ext = self.cert.get_extension(i)
                item_val = item_ext.get_data()[2:].decode('utf-8')
                val_items = item_val.split(':')
                if len(val_items) > 1:
                    ret_obj[val_items[0]] = val_items[1]
                else:
                    ret_obj[val_items[0]] = ''

        return ret_obj

    def get_create_datetime(self):
        return self.cert.get_notBefore()

    def get_expire_datetime(self):
        return self.cert.get_notAfter()

    def get_validity(self):
        ret_dict = {}
        if self.cert is not None:
            b_issue_date = self.cert.get_notBefore()
            if b_issue_date is not None:
                str_issue_date = b_issue_date.decode('utf-8')
                issue_datetime = datetime.strptime(str_issue_date, '%Y%m%d%H%M%SZ')
            else:
                issue_datetime = None

            b_expire_date = self.cert.get_notAfter()
            if b_expire_date is not None:
                str_expire_date = b_expire_date.decode('utf-8')
                expire_datetime = datetime.strptime(str_expire_date, '%Y%m%d%H%M%SZ')
            else:
                expire_datetime = None

            if issue_datetime is not None:
                ret_dict['issue_datetime'] = issue_datetime.strftime('%Y-%m-%d %H:%M:%S')
            if expire_datetime is not None:
                ret_dict['expire_datetime'] = expire_datetime.strftime('%Y-%m-%d %H:%M:%S')

        return ret_dict


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_crt_file = os.path.join(base_dir, 'ssl_crts', '')

    pass
