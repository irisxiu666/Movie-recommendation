import requests

def translate(text, source_lang, target_lang, api_key):
    url = "https://api.niutrans.com/NiuTransServer/translation"
    params = {
        "from": source_lang,
        "to": target_lang,
        "apikey": api_key,
        "src_text": text
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('tgt_text', '')
    else:
        return "Error: " + response.text

# 使用示例
# api_key = 'e23d70681719c399ebcfd8ff1ff17118'  # 替换成你的API密钥
# text = "Hello, world!"
# source_lang = "en"
# target_lang = "zh"
# translation = translate(text, source_lang, target_lang, api_key)
# print(translation)
