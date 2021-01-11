# encoding: utf-8
from abc import ABCMeta, abstractmethod
import datetime
import json
import time

# import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')


# 校验工具类
class ValidateUtil(object):

    def __init__(self):
        self.__name_obj__ = {}
        self.__value_obj__ = {}
        self.__rule_obj__ = {}

    def add(self, key, value, name, rule):
        self.__value_obj__[key] = value
        self.__rule_obj__[key] = rule
        self.__name_obj__[key] = name

    def validate_result(self):
        for key in self.__rule_obj__.keys():
            for i in range(0, len(self.__rule_obj__[key])):
                self.__rule_obj__[key][i].set_value(self.__value_obj__[key])
                valid_result = self.__rule_obj__[key][i].valid()
                if valid_result is not None:
                    return self.__name_obj__[key] + valid_result
        return None


# 校验规则抽象类
class Rule(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.__message = ''
        self.__value = ''

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value
        return None

    def get_message(self):
        return self.__message

    def set_message(self, message):
        self.__message = message
        return None

    @abstractmethod
    def valid(self):
        pass


# 非空校验
class Required(Rule):
    """
    对None和空字符串校验均不通过

    """
    def __init__(self):
        Rule.__init__(self)

    def valid(self):
        if self.get_value() is None or len(self.get_value()) < 1:
            return '不能设置为空值'
        else:
            return None


# 全数字校验
class Numeric(Rule):
    """
    要求校验对象必须全是数字, 不能包含符号和小数点
    """
    def __init__(self):
        Rule.__init__(self)

    def valid(self):
        if self.get_value() is None or len(self.get_value()) < 1:
            return None
        if self.get_value().isdigit():
            return None
        else:
            return '必须是数字'


# 浮点数校验
class Float(Rule):
    """
    浮点数校验, 要求校验对象必须是浮点数
    可以同时校验取值范围
    """
    def __init__(self, gt=None, gte=None, lt=None, lte=None):
        Rule.__init__(self)
        self.__gt_value__ = gt
        self.__gte_value__ = gte
        self.__lt_value__ = lt
        self.__lte_value__ = lte

    def valid(self):
        if self.get_value() is None or len(self.get_value()) < 1:
            return None

        try:
            real_value = float(self.get_value())
            if self.__gt_value__ and real_value <= self.__gt_value__:
                return '必须大于' + self.__gt_value__
            if self.__gte_value__ and real_value < self.__gt_value__:
                return '不能小于' + self.__gte_value__
            if self.__lt_value__ and real_value >= self.__lt_value__:
                return '必须小于' + self.__lt_value__
            if self.__lte_value__ and real_value > self.__lte_value__:
                return '不能大于' + self.__lte_value__
        except ValueError:
            return '必须是浮点数'


# 整数校验
class Int(Rule):
    """
    整数校验, 要求校验对象必须是整数
    可以同时校验取值范围
    """
    def __init__(self, gt=None, gte=None, lt=None, lte=None):
        Rule.__init__(self)
        self.__gt_value__ = gt
        self.__gte_value__ = gte
        self.__lt_value__ = lt
        self.__lte_value__ = lte

    def valid(self):
        if self.get_value() is None or len(self.get_value()) < 1:
            return None

        try:
            real_value = int(self.get_value())
            if self.__gt_value__ and real_value <= self.__gt_value__:
                return '必须大于' + self.__gt_value__
            if self.__gte_value__ and real_value < self.__gt_value__:
                return '不能小于' + self.__gte_value__
            if self.__lt_value__ and real_value >= self.__lt_value__:
                return '必须小于' + self.__lt_value__
            if self.__lte_value__ and real_value > self.__lte_value__:
                return '不能大于' + self.__lte_value__
            return None
        except ValueError:
            return '必须是整数'


# 字符串长度校验
class Length(Rule):
    """
    字符串长度校验
    """
    def __init__(self, min_length=None, max_length=None, length=None):
        Rule.__init__(self)
        self.__min_length__ = min_length
        self.__max_length__ = max_length
        self.__length__ = length

    def valid(self):
        if self.get_value() is None or len(self.get_value()) < 1:
            return None

        if self.__max_length__ and len(self.get_value()) > self.__max_length__:
            return '长度不能大于' + self.__max_length__.__str__()
        if self.__min_length__ and len(self.get_value()) < self.__min_length__:
            return '长度不能小于' + self.__min_length__.__str__()
        if not self.__length__ and len(self.get_value()) == self.__length__:
            return '长度必须是' + self.__length__.__str__()
        return None


# 取值合法性校验
class CheckBox(Rule):
    """
    取值合法性校验
    传入的值需要是一个数组
    """
    def __init__(self, array):
        Rule.__init__(self)
        self.__array__ = array

    def valid(self):
        if self.get_value() is None or len(self.get_value()) < 1:
            return None

        for obj in self.__array__:
            if obj.__str__() == self.get_value():
                return None
        return '不在可选范围内'


# 正则校验
class Regex(Rule):
    """
    正则校验, 允许传入正则表达式
    """
    def __init__(self, regex_rule):
        Rule.__init__(self)
        if isinstance(regex_rule, str):
            import re
            self.__regex_rule__ = re.compile(regex_rule)
        else:
            self.__regex_rule__ = regex_rule

    def valid(self):
        if self.get_value() is None or len(self.get_value()) < 1:
            return None

        if self.__regex_rule__.match(self.get_value()):
            return None
        else:
            return '格式不合法'


# 日期格式校验
class Date(Rule):
    """
    校验日期格式的字符串, 标准格式为2016-01-01
    """
    def __init__(self):
        Rule.__init__(self)

    def valid(self):
        if self.get_value() is None or len(self.get_value()) < 1:
            return None

        try:
            date_format = '%Y-%m-%d'
            datetime.datetime.fromtimestamp(time.mktime(time.strptime(self.get_value(), date_format)))
            return None
        except ValueError:
            return '必须是日期'


# 日期时间格式校验
class Datetime(Rule):
    """
    日期时间格式校验, 标准格式为2016-01-01 00:00:00
    """
    def __init__(self):
        Rule.__init__(self)

    def valid(self):
        if self.get_value() is None or len(self.get_value()) < 1:
            return None

        try:
            datetime_format = "%Y-%m-%d %H:%M:%S"
            datetime.datetime.fromtimestamp(time.mktime(time.strptime(self.get_value(), datetime_format)))
            return None
        except ValueError:
            return '必须是日期时间'


# Json字符串校验
class JsonCheck(Rule):
    def __init__(self):
        Rule.__init__(self)

    def valid(self):
        if self.get_value() is None or len(self.get_value()) < 1:
            return None
        try:
            json.loads(self.get_value())
            return None
        except (TypeError, ValueError):
            return '不是json结构'