# encoding: utf-8

import random
import string
import uuid
import os
import hashlib
import re


def is_url_str(target_str):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', target_str)


def replace_all_symbol(org_str, replacement_char):
    if org_str and len(org_str):
        del_str = string.punctuation + string.digits  # ASCII 标点符号，数字
        replacement = replacement_char * len(del_str)
        tran_tab = str.maketrans(del_str, replacement)

        return org_str.translate(tran_tab)
    else:
        raise Exception('Original string could not be None or empty string.')


def generate_random_num(length=6):
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(length))


def generate_random_str(length=6):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(length))


def is_blank_str(target):
    target = target.strip()
    if target is None or target == '':
        return True
    else:
        return False


def is_int_str(target):
    try:
        int(target)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(target)
        return True
    except (TypeError, ValueError):
        pass
    return False


def is_float_str(target):
    try:
        float(target)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(target)
        return True
    except (TypeError, ValueError):
        pass
    return False


def generate_uuid():
    return uuid.uuid4().__str__()


def depart_write(root, path, depart_symbol="/"):
    print(os.getcwd())
    l = path[:3] + depart_symbol + path[3:6]
    if not os.path.exists(root+l):
        os.makedirs(root+l)
    return root+l+"/"+path


def add1(total_count):
    """
    add_fd3455 -> self
    add_355->add_336
    add_45_54->self
    """
    j = 0
    for i in total_count:
        j += 1
        if i == "_":
            num = total_count[j:]
            if num.isdigit():
                next_num = int(num)+1
                return total_count[:j] + str(next_num)

    return total_count


def get_sha1(src_str):
    return hashlib.sha1(src_str).hexdigest()


def get_sha256(src_str):
    return hashlib.sha3_256(src_str).hexdigest()


def get_md5(org_str):
    if org_str is None:
        return None

    m1 = hashlib.md5()
    m1.update(org_str.encode('utf-8'))
    md5_str = m1.hexdigest()

    return md5_str


if __name__ == '__main__':
    from utils.global_value import ID_IMG_PATH
    print(depart_write(ID_IMG_PATH, "12423566"))
