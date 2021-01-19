# encoding: utf-8

import json
import os
import sys

# from api.models import ExceptionLog, AccessLog
from utils.constants_name_map import error_dict


# # 接口调用返回失败
# def get_fail(error_code, message=None):
#     return {
#         'result': 'FAIL',
#         'code': error_code,
#         'message': message if message else error_dict[error_code]
#     }


# 接口返回成功
def get_ok():
    return {
        'code': '200',
        'message': '',
        'data': {}
    }


def get_param_error(error_message):
    return {
        'code': '1',
        'message': error_message,
    }


# 接口返回失败
def get_fail(error_code='F0001', error_message=''):
    if error_code in error_dict:
        error_message = error_dict[error_code] + ' ' + error_message

    return {
        'code': error_code,
        'message': error_message,
    }


# 网页返回失败
def fail(message=None):
    return {
        'code': 3,
        'message': message if message else None,
        'data': {"id_info": []}
    }


# 网页返回成功
def ok():
    return {
        'result': 'OK',
        'message': ''
    }


# # 记录异常日志
# def save_exception(ex, request=None, ext_msg=None):
#     """
#     Save exception log
#
#     :param ex:          exception stack
#     :param request:     http request, None is allowed
#     :param ext_msg:     exception message, None is allowed
#     :return: True if ex exists, else False
#     """
#     if ex:
#         try:
#             exception = ExceptionLog()
#
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             line_number = str(exc_tb.tb_lineno)
#
#             exception.service = '%s (Line Number: %s)' % (filename, line_number)
#             if request:
#                 exception.module = request.META['PATH_INFO']
#                 if request.method == 'GET':
#                     exception.parameter = json.dumps(dict(request.GET.iterlists()))
#                 elif request.method == 'POST':
#                     exception.parameter = json.dumps(dict(request.POST.iterlists()))
#                 else:
#                     pass
#             else:
#                 exception.module = u'未知文件路径'
#
#             exception.content = ('ext_msg: ' + ext_msg if ext_msg else '') + ' exception: ' + ex.__str__()
#             exception.save()
#
#             return exception
#         except Exception as inner_ex:
#             print(inner_ex.__str__())
#     else:
#         return False
#
#
# # 记录访问日志
# def save_access_log(url, access_type, access_method, response_code=None, param_dict=None, result=None):
#     try:
#         if access_method == 'GET':
#             # Get请求处理参数
#             tmp_list = url.split('?')
#             if len(tmp_list) == 1:
#                 # 请求不带参数
#                 parameters = None
#             else:
#                 url = tmp_list[0]
#                 param_str = tmp_list[1]
#                 parameters = {}
#                 for obj in param_str.split('&'):
#                     parameters[obj.split('=')[0]] = obj.split('=')[1]
#                 parameters = json.dumps(parameters)
#         else:
#             # Post请求处理参数
#             if param_dict:
#                 parameters = json.dumps(param_dict)
#             else:
#                 parameters = None
#
#         # result有中文, 先json解码再转json字符串
#         AccessLog.objects.create(
#             type=access_type, method=access_method,
#             url=url, parameters=parameters,
#             result=json.dumps(json.loads(result), ensure_ascii=False) if result else None,
#             response_code=response_code
#         )
#     except Exception as ex:
#         print(ex.__str__())
