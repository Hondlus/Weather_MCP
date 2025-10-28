from spider.get_city_list import get_city_list
from spider.get_weather_by_cityId import get_weather_by_cityId
import re
from mcp.server import FastMCP
import sys
import locale
import logging


# Ensure UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# #打开debug 日志
# logging.getLogger("strands").setLevel(logging.DEBUG)
# logging.basicConfig(
#     format="%(levelname)s | %(name)s | %(message)s",
#     handlers=[logging.StreamHandler()]
# )

# Create an MCP server
mcp = FastMCP(
    name="Get Weather Service",
    host="0.0.0.0",
    port=8080
)


@mcp.tool()
def get_weather(input_str:str)->dict:
    """这是一个可以获取未来7天天气情况的MCP，你可以输入城市地区来获取未来7天的天气。城市地区的格式：上海市静安区 或者 上海 静安 或者 上海，静安 或者 上海|静安；如果输入上海，则参数为：上海 上海。

    Args:
        input_str: 城市地区的格式：上海市静安区 或者 上海 静安 或者 上海，静安 或者 上海|静安；如果输入上海，则参数为：上海 上海。

    Returns:[['21日11时,d07,小雨,27℃,北风,<3级,3', '21日14时,d07,小雨,29℃,东风,<3级,3', '21日17时,d01,多云,30℃,西风,<3级,2', '21日20时,n00,晴,26℃,南风,<3级,0', '21日23时,n00,晴,20℃,西南风,<3级,0', '22日02时,n01,多云,19℃,北风,<3级,0', '22日05时,n03,阵雨,19℃,西风,<3级,0', '22日08时,d03,阵雨,18℃,北风,<3级,3'], ['22日11时,d03,阵雨,24℃,东北风,<3级,3', '22日14时,d03,阵雨,30℃,东北风,<3级,3', '22日17时,d03,阵雨,31℃,南风,<3级,3', '22日20时,n01,多云,26℃,东北风,<3级,0', '22日23时,n03,阵雨,20℃,东北风,<3级,0', '23日02时,n01,多云,19℃,北风,<3级,0', '23日05时,n01,多云,17℃,东北风,<3级,0', '23日08时,d01,多云,20℃,北风,<3级,2'], ['23日11时,d08,中雨,29℃,东北风,<3级,3', '23日14时,d08,中雨,29℃,东南风,<3级,3', '23日17时,d08,中雨,31℃,东南风,<3级,3', '23日20时,n08,中雨,24℃,东北风,<3级,0', '23日23时,n07,小雨,21℃,东北风,<3级,0', '24日02时,n07,小雨,20℃,东北风,<3级,0', '24日05时,n07,小雨,19℃,北风,<3级,0', '24日08时,d02,阴,18℃,北风,<3级,3'], ['24日14时,d07,小雨,31℃,东风,<3级,3', '24日20时,n07,小雨,25℃,东南风,<3级,0', '25日02时,n08,中雨,19℃,东北风,<3级,0', '25日08时,d07,小雨,19℃,东北风,<3级,3'], ['25日14时,d07,小雨,31℃,东南风,<3级,3', '25日20时,n08,中雨,26℃,东南风,<3级,0', '26日02时,n07,小雨,21℃,东风,<3级,0', '26日08时,d08,中雨,18℃,北风,<3级,3'], ['26日14时,d08,中雨,30℃,南风,<3级,3', '26日20时,n08,中雨,25℃,东风,<3级,0', '27日02时,n09,大雨,21℃,东风,<3级,0', '27日08时,d08,中雨,19℃,东风,<3级,3'], ['27日14时,d08,中雨,25℃,西南风,<3级,3', '27日20时,n09,大雨,25℃,南风,<3级,0', '28日02时,n08,中雨,20℃,东北风,<3级,0', '28日08时,d07,小雨,18℃,东北风,<3级,0']]
    """
    # 清洗输入：去除"市"、"区"，分割城市和区
    city,district=parse_location(input_str)
    data = get_city_list()
    result=[item for item in data
            if item['city_cn'] == city
            and item['district_cn'] == district]
    if result:
        return {"getweather": get_weather_by_cityId(result[0]['city_id'])}
    else:
        return ''

def parse_location(input_str):
    # 统一处理所有可能的分隔符（空格、逗号、顿号、斜杠、竖线等）
    # 并移除"市"和"区"字样
    cleaned=re.sub(r'[、，,/|]',' ',input_str)  # 将所有分隔符替换为空格
    cleaned=re.sub(r'市|区','',cleaned)  # 移除"市"和"区"
    cleaned=re.sub(r'\s+',' ',cleaned).strip()  # 合并多余空格

    # 分割城市和区域
    parts=cleaned.split(' ',1)  # 最多分割一次

    if len(parts) == 2:
        city,district=parts
    elif len(parts) == 1: #只输入了省
        city,district=cleaned,cleaned
    elif len(cleaned) > 2:  # 处理没有分隔符的情况（如"上海静安"）
        city=cleaned[:2]  # 假设城市名是前两个字
        district=cleaned[2:]
    else:
        city,district=cleaned,''  # 默认值

    return city,district


# Start the MCP server
if __name__ == "__main__":
    print("Starting Get Weather MCP Server...")
    mcp.run(transport="streamable-http")
    # mcp.run(transport="sse")