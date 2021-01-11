# encoding: utf-8

import multiprocessing
import os

from datetime import datetime
from pki_services import settings
from service import services, ocsp_server
from utils import x509_cert_utils

if __name__ == '__main__':
    multiprocessing.freeze_support()
    # serial_no, paths = services.generate_certificate({'uid': '123123123', 'gid': ['123123', '0987654321']})
    # print(serial_no)
    # print(paths)
    # print()
    #
    # services.revoke_cert_file(serial_no)

    # ocsp_server.start_ocsp_server()

    # print(services.verify_cert_serial_no(269488169))

    # print(services.verify_cert_file(os.path.join(settings.BASE_DIR, 'ssl_crts', '10101029', '10101029_cert.pem')))

    cert_utils = x509_cert_utils.X509CertUtils()
    cert_utils.load_pem(os.path.join(settings.BASE_DIR, 'ssl_crts', '10101029', '10101029_cert.pem'))

    create_datetime_str = cert_utils.get_create_datetime().decode('utf-8')[:-1]
    create_datetime = datetime.strptime(create_datetime_str, '%Y%m%d%H%M%S')
    print(create_datetime.strftime('%Y-%m-%d %H:%M:%S'))
