import requests
import json
import random
import hashlib
from urllib.parse import quote

# 百度翻译API的URL
BAIDU_TRANSLATE_URL = 'https://api.fanyi.baidu.com/api/trans/vip/translate'


# 生成随机数的方法
def make_salt():
    return str(random.randint(32768, 65536))


# 签名生成方法
def make_sign(appid, query, salt, secretKey):
    sign = appid + query + salt + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode('utf-8'))
    return m1.hexdigest()


# 获取access token
def get_baidu_translation(appid, secretKey, query, from_lang='zh', to_lang='en'):
    salt = make_salt()
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    sign = make_sign(appid, query, salt, secretKey)

    # 构建请求参数
    payload = {
        'q': query,
        'from': from_lang,
        'to': to_lang,
        'appid': appid,
        'salt': salt,
        'sign': sign
    }

    # 发起请求
    r = requests.post(BAIDU_TRANSLATE_URL, params=payload, headers=headers)
    # 解析结果
    result = r.json()

    # 打印结果
    if "trans_result" in result:
        # print(result["trans_result"][0]["src"])
        # print(result["trans_result"][0]["dst"])
        return result["trans_result"][0]["dst"]
    else:
        print("Error:", result)
        return None


# # 使用百度翻译的示例
# appid = '20220128001069914'  # 替换为你的appid
# secretKey = 'upJXF9j4oKevKHsv7_7q'  # 替换为你的密钥
#
# # 测试翻译的文本
# text_to_translate = '你好世界'
# translated_text = get_baidu_translation(appid, secretKey, text_to_translate)
#
# print("Translated text:", translated_text)
