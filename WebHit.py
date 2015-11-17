#! /usr/bin/env python
# coding: utf-8

import json
import base64
import urllib
import urllib2


username = "zgV2yQRb/Mxe+v7yT/+fj+bXrSG8WOed/WuxCLwQ/5o"
password = "zgV2yQRb/Mxe+v7yT/+fj+bXrSG8WOed/WuxCLwQ/5o"
quote = "%27"

#認証と接続
def track_stream(username, password, keyword):
    url = "https://api.datamarket.azure.com/Bing/SearchWeb/v1/Composite?"
    params = "$format=json" + "&Query=" + quote + urllib2.quote(keyword.encode('utf-8')) + quote
    request_url = url + params 

    # Basic認証用のパスワードマネージャーを作成
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, username, password)

    # openerの作成とインストール
    # HTTPS通信とBasic認証用のHandlerを使用
    opener = urllib2.build_opener(urllib2.HTTPSHandler(),
                                  urllib2.HTTPBasicAuthHandler(password_mgr))
    urllib2.install_opener(opener)

    # 接続
    #request = urllib2.Request(url, data)
    response =  urllib2.urlopen(request_url)
    return response

#json形式のソート
def json_analyze(r):
	jsondata = json.load(r)  #Json形式で入手
	result = jsondata["d"]
	result = result["results"]
	for item in result:
		hitnum = item["WebTotal"]


	#見やすくしただけ
	sort = json.dumps(result, sort_keys = True, ensure_ascii=False, indent = 4)
	sort = sort.encode('utf-8')

	return hitnum


if __name__ == '__main__':
    res = track_stream(username, password, "python")
    r = json_analyze(res)
    print r