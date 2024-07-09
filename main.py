from pkg.plugin.context import (
    register,
    handler,
    llm_func,
    BasePlugin,
    APIHost,
    EventContext,
)
from pkg.plugin.events import NormalMessageResponded   # 导入事件类
from mirai import Image, MessageChain
import re
import httpx
import random
import logging

# 注册插件


@register(name="weather", description="Weather", version="0.1", author="zzseki")
class WeatherPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.token = "Zgv6hD2FyDYrPGGF"  # 请将这里的'YOUR_TOKEN'替换为你实际获取的token
        self.logger = logging.getLogger(__name__)


    @handler(NormalMessageResponded)
    async def normal_message_responded(self, ctx: EventContext, **kwargs):
        response_text = ctx.event.response_text
        #今天|明天|后天|大后天|一天后|两天后|三天后|四天后|五天后|1天后|2天后|3天后|4天后|5天后|6天后

        # 定义正则表达式模式，匹配形如 城市:xxx 的字符串
        CITY_PATTERN = re.compile(r"城市:(.*?)(今天|明天|后天|大后天|一天后|两天后|三天后|四天后|五天后|六天后|1天后|2天后|3天后|4天后|5天后|6天后)的天气情况")
        #TIME_PATTERN = re.compile(r"为你查询城市：\w+([^天]+)天的天气情况")

        match = CITY_PATTERN.search(response_text)
        # 如果找到匹配的字符串，则处理
        if match:
            if match.group(2) == "今天" or match.group(2) == "0" or match.group(2) == "零":
                W_time = 0  # 0表示当天的天气，1表示明天的天气，以此类推最高查询七天



            elif match.group(2) == "明天" or match.group(2) == "1天后" or match.group(2) == "一天后":
                W_time = 1


            elif match.group(2) == "后天" or match.group(2) == "2天后" or match.group(2) == "二天后" or match.group(
                    2) == "两天后":
                W_time = 2


            elif match.group(2) == "大后天" or match.group(2) == "3天后" or match.group(2) == "三天后":
                W_time = 3


            elif match.group(2) == "大大后天" or match.group(2) == "4天后" or match.group(2) == "四天后":
                W_time = 4


            elif match.group(2) == "大大大后天" or match.group(2) == "5天后" or match.group(2) == "五天后":
                W_time = 5


            elif match.group(2) == "大大大大后天" or match.group(2) == "6天后" or match.group(2) == "六天后":
                W_time = 6

            else:
                W_time = 0

        # 如果找到匹配的字符串，则处理
        if match:
            city = match.group(1)

            #for city in match.group(1):

                # 处理每一个匹配到的城市名称

            self.logger.info(city)
            text = await self.get_weather(city, W_time)

            if text:
                await ctx.event.query.adapter.reply_message(
                    ctx.event.query.message_event, [(text)], False
                )
            else:
                self.logger.warning("没有找到符合条件的城市信息。")

    async def get_weather(self, city, W_time):
        url = "https://v2.alapi.cn/api/tianqi/seven"
        params = {
            "token": self.token,
            "city": city,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

        data = response.json()["data"]
        day_weather = data[W_time]
        if day_weather:

            city = day_weather['city']                        #城市名称
            date = day_weather['date']                        #日期
            province = day_weather['province']                #省份
            temp_day = day_weather['temp_day']                #白天温度
            temp_night = day_weather['temp_night']            #夜晚温度
            wea_day = day_weather['wea_day']                  #白天天气
            wea_night = day_weather['wea_night']              #夜晚天气
            wind_day = day_weather['wind_day']                #白天风向
            wind_night = day_weather['wind_night']            #夜晚风向
            wind_day_level = day_weather['wind_day_level']    #白天风力等级
            wind_night_level = day_weather['wind_night_level']#夜晚风力等级
            air = day_weather['air']                          #空气质量指数
            air_level = day_weather['air_level']              #空气质量级别
            precipitation = day_weather['precipitation']      #降水量
            sunrise = day_weather['sunrise']                  #日出时间
            sunset = day_weather['sunset']                    #日落时间
            result = (f"省份：{province}\n城市：{city}\n日期：{date}\n"
                      f"白天天气：{wea_day}\n白天温度：{temp_day}\n白天风向：{wind_day}\n"
                      f"白天风力等级：{wind_day_level}\n夜晚天气：{wea_night}\n夜晚温度：{temp_night}\n"
                      f"夜晚风向：{wind_night}\n夜晚风力等级：{wind_night_level}\n空气质量指数：{air}\n"
                      f"空气质量级别：{air_level}\n降水量：{precipitation}\n日出时间：{sunrise}\n日落时间：{sunset}")

            return result
        else:
            return None

    

    # 插件卸载时触发
    def __del__(self):
        pass
