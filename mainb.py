# -*- coding: utf-8 -*-
 
import discord
from discord.ext import commands
import traceback
import requests
import xml.etree.ElementTree as ET
import urllib
import urllib.request
import json
 
# http接続する関数
def httpRequest(url, params):
    # 正式なurlに変換
    parseUrl = "{}?{}".format(url, urllib.parse.urlencode(params))
    # リクエストを作成
    req = urllib.request.Request(parseUrl)
    with urllib.request.urlopen(req) as res:
        # 結果を代入
        body = res.read()
    # 返却
    return body
 
# main処理を行う関数
def main():
 
    # http接続してapiからjsonを取得
    res = httpRequest(
        "https://api.p2pquake.net/v1/human-readable",
        {
            "limit": 10,
            "code": 551
        }
    )
    # jsonをpythonで扱える辞書型形式に変換する
    doc = json.loads(res)
 
    # 辞書型をloopで回して1件の情報を取得
    for val in doc:
        # earthquakeが存在しない場合は処理をスキップ
        if val.get("earthquake") == None: continue
        # 震度
        intensity = val.get("earthquake").get("maxScale")
        #震度5弱より大きいか小さいか判断 (45=震度5弱 / APIより)
        if intensity >= 45:
            # 震度5弱以上 緊急地震速報発令とみなす
            if intensity == 45:
                print("震度5弱")
            elif intensity == 50:
                print("震度5強")            
            elif intensity == 55:
                print("震度6弱")
            elif intensity == 60:
                print("震度6強")
            elif intensity == 70:
                print("震度7")
        else:
            # 震度5弱以下 未発令とみなす
            if intensity == 0:
                print("震度0")
            elif intensity == 10:
                print("震度1")
            elif intensity == 20:
                print("震度2")
            elif intensity == 30:
                print("震度3")
            elif intensity == 40:
                print("震度4")
 
# main関数を実行
main()
INITIAL_EXTENSIONS = [
    'cogs.cmd'
]
def e():
    xml_data_module = requests.get('https://www3.nhk.or.jp/sokuho/jishin/data/JishinReport.xml')
    xml_data_module.encoding = "Shift_JIS"
    root = ET.fromstring(xml_data_module.text)
    for item in root.iter('item'):
       deta_url = (item.attrib['url'])
       break
    deta = requests.get(deta_url)
    deta.encoding = "Shift_JIS"
    root = ET.fromstring(deta.text)
    e_1 = ''
    for Earthquake in root.iter('Earthquake'):
        time = (Earthquake.attrib['Time'])
        Intensity = (Earthquake.attrib['Intensity'])
        Epicenter = (Earthquake.attrib['Epicenter'])
        Magnitude = (Earthquake.attrib['Magnitude'])
        Depth = (Earthquake.attrib['Depth'])
        map_url = 'https://www3.nhk.or.jp/sokuho/jishin/'
        count = 1
    for Area in root.iter('Area'):
        e_1 += '\n' + Area.attrib['Name']
        if count == 10:
            e_1 += '\n他'
            break
        count = count + 1
    for Detail in root.iter('Detail'):
        map = map_url + Detail.text
        edic = {'time': time, 'epicenter': Epicenter, "intensity": Intensity, "depth": Depth, "magnitude": Magnitude, "map": map, "icon": eicon(Intensity), "color": eicolor(Intensity), 'e_1': e_1}
        return edic
 
def eicon(i):
    if i == '1':
        return('https://i.imgur.com/yalXlue.png')
    elif i == '2':
        return('https://i.imgur.com/zPSFvj6.png')
    elif i == '3':
        return('https://i.imgur.com/1DVoItF.png')
    elif i == '4':
        return("https://i.imgur.com/NqC3CE0.png")
    elif i == '5-':
        return("https://i.imgur.com/UlFLa3G.png")
    elif i == '5+':
        return("https://i.imgur.com/hExQwf2.png")
    elif i == '6-':
        return("https://i.imgur.com/p9RrO96.png")
    elif i == '6+':
        return("https://i.imgur.com/pNaFJ2Y.png")
    elif i == '7':
        return("https://i.imgur.com/ZoOhL4v.png")
 
def eicolor(i):
    if i == '1':
        return(0x51b3fc)
    elif i == '2':
        return(0x7dd45a)
    elif i == '3':
        return(0xf0ed7e)
    elif i == '4':
        return(0xfa782c)
    elif i == '5-':
        return(0xb30f20)
    elif i == '5+':
        return(0xb30f20)
    elif i == '6-':
        return(0xffcdde)
    elif i == '6+':
        return(0xffcdde)
    elif i == '7':
        return(0xffff6c)
class MyBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()
 
    async def on_ready(self):
        print('BOT起動')
 
if __name__ == '__main__':
    bot = MyBot(command_prefix='.')
    bot.run('')
