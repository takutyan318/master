#! /usr/bin/env python
# coding: utf-8

import json
import base64
import urllib
import urllib2
import xml.etree.ElementTree as ET


username = "zgV2yQRb/Mxe+v7yT/+fj+bXrSG8WOed/WuxCLwQ/5o"
password = "zgV2yQRb/Mxe+v7yT/+fj+bXrSG8WOed/WuxCLwQ/5o"

#認証と接続
def track_stream(username, password, keyword):
    quote = "%27"
    url = "https://api.datamarket.azure.com/Bing/Search/v1/Composite?"
    params = "Sources=" + quote + "web" + quote + "&Query=" + quote + urllib2.quote(keyword.encode('utf-8')) + quote
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

def xml_analyze(data):
    tree = ET.parse(data)
    root = tree.getroot()
    for node in root.getchildren():
        if node.tag == "{http://www.w3.org/2005/Atom}entry":
            for subnode in node.getchildren():
                if subnode.tag == "{http://www.w3.org/2005/Atom}content":
                    for sub2node in subnode.getchildren():
                        if sub2node.tag == "{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties":
                            for sub3node in sub2node.getchildren():
                                if sub3node.tag == "{http://schemas.microsoft.com/ado/2007/08/dataservices}WebTotal":
                                    total = sub3node.text

    return total
    


if __name__ == '__main__':
    res = track_stream(username, password, u"奇抜でおかしい")
    wtotal = xml_analyze(res)
    print wtotal
    

