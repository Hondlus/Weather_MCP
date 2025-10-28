import requests
import time
import re
import json
#https://toy1.weather.com.cn/search?cityname=上海 获取城市编码
# url='https://toy1.weather.com.cn/search'
#实时获取城市对应天气查询的city_id
def get_city_list()-> list[dict]:
    city_list=["北京","上海","天津","重庆","黑龙江","吉林","辽宁","内蒙古","河北","山西","陕西","山东","新疆","西藏","青海","甘肃","宁夏","河南","江苏","湖北","浙江","安徽","福建","江西","湖南","贵州","四川","广东","云南","广西","海南"]
    url = "https://toy1.weather.com.cn/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "Referer": "https://www.weather.com.cn/",
    }
    parsed_data=[]
    for i in city_list:
        params={
            "cityname":i,
            "callback":f"jQuery{int(time.time() * 1000)}_{int(time.time() * 1000)}",
            "_":int(time.time() * 1000),
        }

        resp = requests.get(url, params=params, headers=headers)
        # 去掉 jQuery 回调部分，提取 JSON
        data = re.sub(r'^jQuery\d+_\d+\(|\)$', '', resp.text)
        for item in json.loads(data):
            parts=item["ref"].split("~")
            parsed_data.append({
                "city_id":parts[0],  # 101010100
                "city_cn":parts[9],  # 北京
                "city_en":parts[1],
                "district_cn":parts[2],  # 北京
                "district_en":parts[3]  # Beijing
                # "province_code":parts[6],  # 10
                # "postal_code":parts[7],  # 100000
                # "short_code":parts[8],  # BJ

            })
    return parsed_data