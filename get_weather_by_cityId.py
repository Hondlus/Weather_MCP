import requests
import re
import json
#从天气网https://www.weather.com.cn/获取天气预报
# url='https://www.weather.com.cn/'
#实时获取城市对应天气查询的city_id
def get_weather_by_cityId(city_id:str)-> list[dict]:
    url = f"https://www.weather.com.cn/weather/{city_id}.shtml"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "Referer": "https://www.weather.com.cn/",
    }
    resp=requests.get(url,headers=headers)
    resp.encoding="utf-8"
    # 使用正则表达式匹配 hour3data 后面的 JSON
    match=re.search(r'var hour3data=({.*?});?',resp.text,re.DOTALL)
    if match:
        json_str=match.group(1)  # 提取匹配的JSON字符串
        data=json.loads(json_str)  # 解析为Python字典
        return data['7d']
    else:
        return []
