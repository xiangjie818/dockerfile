# encoding: utf-8

import base64
import json
import os
import traceback
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from utils.decorator import qd_compose, qd_validator, qd_http_response
from utils.validator import Required, Numeric, Int
from utils import view_utils, constants, string_utils
from utils import x509_cert_utils

from service import services
from pki_services.settings import BASE_URL, VERIFY_CERT_FILE


"""
@apiDefine ApiModule
PKI API
"""


# @qd_compose(require_GET, csrf_exempt)
@csrf_exempt
def hello(request):
    return qd_http_response(request, view_utils.get_ok())


@qd_compose(require_POST, csrf_exempt, qd_validator([
    ['validity_days', '有效期 (validity_days)', [Required(), Int(gt=1)]],
    ['ext_param', '证书扩展字段 (ext_param)', [Required()]],
]))
def generate_cert(request):
    """
    @api {20010} /pki/generate_cert 申请生成新客户端证书
    @apiName 20010
    @apiGroup ApiModule
    @apiVersion 0.1.0
    @apiDescription 生成客户端证书，ext_param参数中的内容以证书扩展字段方式写入证书1.2.3.411中

    @apiParam {Integer} validity_days 有效期，单位：天
    @apiParam {String}  ext_param 证书扩展字段内容，JSON 字符串
    @apiParamExample {json} ext_param
    {
        "uid": "",              // 用户唯一id
        "gids": ["", ""]        // 用户所有所在组id
    }

    @apiSuccess {Integer} code 返回代码，200-成功，1-异常，2 -参数错误
    @apiSuccess {String} message 返回消息
    @apiSuccess {String} data 返回数据

    @apiSuccessExample {json} Success-Response:
    {
        "code": "200",
        "message": "",
        "data": {
            "cert_serial_no": "",       // 证书序号，以此作为吊销证书接口参数
            "cert_create_datetime": "", // '%Y-%m-%d %H:%M:%S'
            "cert_expire_datetime": "", // '%Y-%m-%d %H:%M:%S'
            "private_key": "",          // 证书密钥内容base64字符串
            "cert": "",                 // 客户端证书内容base64字符串
            "private_key_pem_path": "",  // .pem格式密钥文件下载链接
            "cert_pem_path": "",         // .pem格式证书文件下载链接
            "ca_cert_pem_path": "",      // .pem CA证书文件下载链接
            "p12_path": "",              // 包含证书和密钥以及CA证书的pkcs12文件下载链接
            "key_file_path": "",         // .key格式密钥文件
            "crt_file_path": "",         // .crt格式证书文件下载链接
        }
    }

    """
    ret_map = view_utils.get_ok()

    try:
        str_validity = request.POST.get('validity_days')
        str_ext_param = request.POST.get('ext_param', '')

        try:
            ext_param = json.loads(str_ext_param)
        except ValueError:
            ext_param = None
            ret_map = view_utils.get_param_error('参数 ext_param 必须是一个json字符串')

        if ext_param is not None:
            validity = int(str_validity)

            serial_no, paths = services.generate_certificate(ext_param=ext_param, validity=validity)

            base64_key = ''
            if os.path.exists(paths['client_pem_key']):
                key_file_content = ''
                with open(paths['client_pem_key'], 'r') as client_key_file:
                    for line in client_key_file:
                        key_file_content += line
                    print(key_file_content)
                    base64_key = base64.b64encode(key_file_content.encode('utf-8')).decode('utf-8')

            base64_cert = ''
            if os.path.exists(paths['client_pem_cert']):
                cert_file_content = ''
                with open(paths['client_pem_cert'], 'r') as client_cert_file:
                    for line in client_cert_file:
                        cert_file_content += line
                    print(cert_file_content)
                    base64_cert = base64.b64encode(cert_file_content.encode('utf-8')).decode('utf-8')

            cert_utils = x509_cert_utils.X509CertUtils()
            cert_utils.load_pem(paths['client_pem_cert'])
            cert_create_dt_str = cert_utils.get_create_datetime().decode('utf-8')[:-1]
            cert_create_dt = datetime.strptime(cert_create_dt_str, '%Y%m%d%H%M%S')

            cert_expire_dt_str = cert_utils.get_expire_datetime().decode('utf-8')[:-1]
            cert_expire_dt = datetime.strptime(cert_expire_dt_str, '%Y%m%d%H%M%S')

            ret_map['data'] = {
                # 证书序号，以此作为吊销证书接口参数
                "cert_serial_no": serial_no,
                # 证书创建时间
                "cert_create_datetime": cert_create_dt.strftime('%Y-%m-%d %H:%M:%S'),
                # 证书过期时间
                "cert_expire_datetime": cert_expire_dt.strftime('%Y-%m-%d %H:%M:%S'),
                # 证书密钥内容base64字符串
                "private_key": base64_key,
                # 客户端证书内容base64字符串
                "cert": base64_cert,
                # .pem格式密钥文件下载链接
                "private_key_pem_path": paths['client_pem_key'],
                # .pem格式证书文件下载链接
                "cert_pem_path": paths['client_pem_cert'],
                # .pem CA证书文件下载链接
                "ca_cert_pem_path": paths['ca_pem_cert'],
                # 包含证书和密钥以及CA证书的 PKCS12 文件下载链接
                "p12_path": paths['client_p12'],
                # .key格式密钥文件
                "key_file_path": paths['client_key_key'],
                # .crt格式证书文件下载链接
                "crt_file_path": paths['client_crt_cert'],
            }
    except Exception as ex:
        print(ex.__str__())
        print(traceback.format_exc())
        ret_map['result'] = constants.FAILURE
        ret_map['message'] = u'系统级错误，'

    return qd_http_response(request, ret_map)


@qd_compose(require_POST, csrf_exempt, qd_validator([
    ['cert_serial_no', '证书序列号 (cert_serial_no)', [Required()]],
]))
def revoke_cert(request):
    """
    @api {20011} /pki/revoke_cert 吊销客户端证书
    @apiName 20011
    @apiGroup ApiModule
    @apiVersion 0.1.0
    @apiDescription 根据证书序列号吊销证书

    @apiParam {Integer} cert_serial_no 证书序列号

    @apiSuccess {Integer} code 返回代码，200-成功，1-异常，2 -参数错误
    @apiSuccess {String} message 返回消息

    """
    ret_map = view_utils.get_ok()

    try:
        cert_serial_no = request.POST.get('cert_serial_no')

        services.revoke_cert_file(cert_serial_no)

    except Exception as ex:
        print(ex.__str__())
        print(traceback.format_exc())
        ret_map['result'] = constants.FAILURE
        ret_map['message'] = u'系统级错误，'

    return qd_http_response(request, ret_map)


@qd_compose(require_POST, csrf_exempt, qd_validator([
    ['cert_serial_no', '证书序列号 (cert_serial_no)', [Required()]],
]))
def verify_cert(request):
    """
    @api {20012} /pki/verify_cert 根据证书序列号验证证书吊销状态
    @apiName 20012
    @apiGroup ApiModule
    @apiVersion 0.1.0
    @apiDescription 根据证书序列号验证证书是否被吊销，并不验证证书是否过期

    @apiParam {Integer} cert_serial_no 证书序列号

    @apiSuccess {Integer} code 返回代码，200-成功，1-异常，2 -参数错误
    @apiSuccess {String} message 返回消息
    @apiSuccess {String} data 返回数据
    @apiSuccessExample {json} Success-Response:
    {
        "is_valid": "",             // 0- 证书已被吊销，1- 合法证书
    }
    """
    ret_map = view_utils.get_ok()

    try:
        cert_serial_no = request.POST.get('cert_serial_no')

        verify_result = services.verify_cert_serial_no(cert_serial_no)
        if verify_result is True:
            is_valid = '1'
        else:
            is_valid = '0'

        ret_map['data'] = {
            'is_valid': is_valid
        }
    except Exception as ex:
        print(ex.__str__())
        print(traceback.format_exc())
        ret_map['result'] = constants.FAILURE
        ret_map['message'] = u'系统级错误，'

    return qd_http_response(request, ret_map)


@csrf_exempt
def verify_cert_file(request):
    """
    @api {20013} /pki/verify_cert_file 根据上传证书文件验证证书吊销状态
    @apiName 20013
    @apiGroup ApiModule
    @apiVersion 0.1.0
    @apiDescription 根据上传证书文件验证证书吊销状态，并不验证证书是否过期

    @apiParam {File} cert_file 证书文件，pem或p12格式

    @apiSuccess {Integer} code 返回代码，200-成功，1-异常，2 -参数错误
    @apiSuccess {String} message 返回消息
    @apiSuccess {String} data 返回数据
    @apiSuccessExample {json} Success-Response:
    {
        "is_valid": "",             // 0- 证书已被吊销，1- 合法证书
    }
    """
    ret_map = view_utils.get_ok()

    try:
        cert_file = request.FILES.get('cert_file')
        if cert_file is None:
            ret_map = view_utils.get_fail(constants.PARAM_ERR, error_message=" 请上传证书文件")
        else:
            org_cert_file_path = os.path.join(VERIFY_CERT_FILE, cert_file.name)
            ext_names = os.path.splitext(org_cert_file_path)
            cert_file_ext_name = ""
            if len(ext_names) > 1:
                cert_file_ext_name = ext_names[1]

            new_cert_file_name = string_utils.generate_random_str(10) + cert_file_ext_name
            new_cert_file_path = os.path.join(VERIFY_CERT_FILE, new_cert_file_name)
            with open(os.path.join(new_cert_file_path), 'wb') as file_handler:
                for chunk in cert_file.chunks():
                    file_handler.write(chunk)

            verify_result = services.verify_cert_file(new_cert_file_path)
            if verify_result is True:
                is_valid = '1'
            else:
                is_valid = '0'

            ret_map['data'] = {
                'is_valid': is_valid
            }

    except Exception as ex:
        print(ex.__str__())
        print(traceback.format_exc())
        ret_map['result'] = constants.FAILURE
        ret_map['message'] = u'系统级错误，'

    return qd_http_response(request, ret_map)


@qd_compose(require_POST, csrf_exempt, qd_validator([
    ['cert_serial_no', '证书序列号 (cert_serial_no)', [Required()]],
]))
def query_cert_url(request):
    """
    @api {20014} /pki/query_cert_url 根据证书序列号获取证书文件下载地址
    @apiName 20014
    @apiGroup ApiModule
    @apiVersion 0.1.0
    @apiDescription 根据上传证书文件验证证书吊销状态，并不验证证书是否过期

    @apiParam {String} cert_serial_no 证书序列号

    @apiSuccess {Integer} code 返回代码，200-成功，1-异常，2 -参数错误
    @apiSuccess {String} message 返回消息
    @apiSuccess {String} data 返回数据
    @apiSuccessExample {json} Success-Response:
    {
            "private_key_pem_url": "",  // .pem格式密钥文件下载链接
            "cert_pem_url": "",         // .pem格式证书文件下载链接
            "ca_cert_pem_url": "",      // .pem CA证书文件下载链接
            "p12_url": "",              // 包含证书和密钥以及CA证书的pkcs12文件下载链接
            "key_file_url": "",         // .key格式密钥文件
            "crt_file_url": "",         // .crt格式证书文件下载链接
            "ca_crt_file_url": "",      // .crt 格式CA证书文件下载链接
    }
    """
    ret_map = view_utils.get_ok()

    try:
        pass
    except Exception as ex:
        print(ex.__str__())
        print(traceback.format_exc())
        ret_map['result'] = constants.FAILURE
        ret_map['message'] = u'系统级错误，'

    return qd_http_response(request, ret_map)
