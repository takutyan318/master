#! /usr/bin/env python
# coding: utf-8

#APIを使わずにブラウザから直接ヒット件数を取得する

import base64
import urllib
import urllib2
import json

class Websearch(object):
	def track_stream(self, keyword):
		#url作成
		api_key = 'AIzaSyCVIuP7wUp-GO4AXd1zIcfNlh0ZknyF9H4'
		engine_id = '015434107178586177863:y9gv9-dvdtc'
		baseUrl = 'https://www.googleapis.com/customsearch/v1?'
		para = {'key':api_key, 'cx':engine_id, 'q':keyword.encode('utf8')}
		url = baseUrl + urllib.urlencode(para)

		#url読み込み
		response = urllib2.urlopen(url)
		content = response.read()  
		obj = json.loads(content)
		queries = obj['queries']
		request = queries['request']
		req = request[0]
		totalResults = req['totalResults']  #type : unicode
		return int(totalResults)

if __name__ == '__main__':
	k = u'筑波大学'
	search = Websearch()
	ans = search.track_stream(k)
	

