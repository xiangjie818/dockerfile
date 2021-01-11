# encoding: utf-8

error_dict = {
    '00000': u'成功',
    'F0001': u'系统错误',
    'F0003': u'Token不正确',

    'E0004': u'签名已过期',
    'E0005': u'签名错误',
    'E0006': u'令牌错误',
    'E0007': u'接口不支持GET调用(GET method is not supported)',
    'E0008': u'接口不支持POST调用(POST method is not supported)',
    'E0009': u'参数错误',

    'E1000': u'接口调用错误',

    'E1101': u'调用网力登录接口异常',
    'E1102': u'调用网力接口认证失败',

    # E2001 - E2100 库管理错误码区段
    'E2001': u'已有相同的库名',
    'E2002': u'请提供库名',
    'E2003': u'无法找到人脸库',

    # E2101 - E2200 人脸业务错误码区段
    'E2101': u'图片中未检测到人脸(does not contain face)',
    'E2102': u'图片中检测到多张人脸(multiple faces contained)',
    'E2103': u'无法找到上传的原始图片(original face image not found)'
}


class ClassifyAlgorithm:
    SVM = 1
    KNN = 2
    NMSLIB = 3

    algorithm_dict = {
        1: 'SVM',
        2: 'KNN',
        3: 'NMSLIB'
    }


# from db_struct_keyname import DBTableKeyName
class IdInfoCacheDbKeyMap:
    def __init__(self):
        self.image_id = "image_id"
        self.idcard = "idcard"
        self.score = "score"


class ImageIdTracking:
    def __init__(self):
        self.table_map = {
            "table_name": "image_id_tracking",
            "image_id": "image_id"
        }

