# encoding: utf-8

import json
from functools import wraps
from django.http import HttpResponse
from django.utils.decorators import available_attrs

from utils.view_utils import *
from utils.validator import ValidateUtil
from utils import constants


def qd_http_response(request, result):
    """
    需要记录接口日志时调用
    :param request:
    :param result:
    :param is_ali:
    :return:
    """
    if not isinstance(result, dict):
        return HttpResponse(result, content_type="application/json")

    result_str = json.dumps(result, ensure_ascii=False)
    if 0:
        param_dict = dict(request.GET)
    else:
        param_dict = dict(request.POST)
    # # 记录接口日志
    # save_access_log(
    #     request.get_full_path(),
    #     1,
    #     request.method, response_code=200,
    #     param_dict=param_dict,
    #     result=result_str
    # )
    return HttpResponse(result_str, content_type="application/json")


def qd_compose(*functions):
    """
    多个装饰器合并装饰器, 执行顺序为: 排在前面的装饰器是最外层
    :param functions:
    :return:
    """
    def deco(f):
        for fun in reversed(functions):
            f = fun(f)
        return f
    return deco


def qd_validator(validate_list):
    """
    参数验证装饰器
    :param validate_list:
    :return:
    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            # 校验参数
            v = ValidateUtil()
            if request.method == 'POST':
                for obj in validate_list:
                    v.add(obj[0], request.POST.get(obj[0], ''), obj[1], obj[2])
            else:
                for obj in validate_list:
                    v.add(obj[0], request.GET.get(obj[0], ''), obj[1], obj[2])

            valid_str = v.validate_result()
            if valid_str:
                return qd_http_response(request, get_fail(constants.PARAM_ERR, error_message=valid_str))
            return func(request, *args, **kwargs)
        return inner
    return decorator

