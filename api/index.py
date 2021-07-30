# -*- codeing = utf-8 -*-
# @Author : noionion
# @Software : PyCharm

import leancloud
from http.server import BaseHTTPRequestHandler
import json
import datetime
import os

from leancloud import user

def getdata():
    list = ['title','time','updated','link','author','headimg']
    list_user = ['frindname','friendlink','firendimg','error']
    # Verify key
    leancloud.init("9IXXGBgDfpll1oh3mX6ktaM9-MdYXbMMI", "r5FYd3er2o0YTFPxdeeXPOdH")
    # leancloud.init(os.environ["LEANCLOUD_ID"], os.environ["LEANCLOUD_KEY"])

    # Declare class
    Friendspoor = leancloud.Object.extend('friend_poor')

    # Create an alias for the query
    query = Friendspoor.query

    # Select the sort methods
    query.descending('time')

    # Limit the number of queries
    query.limit(1000)

    # Choose class
    query.select('title','time','updated','link','author','headimg','createdAt')

    # Execute the query, returning result
    query_list = query.find()

    Friendlist = leancloud.Object.extend('friend_list')
    query_userinfo = Friendlist.query
    query_userinfo.limit(1000)
    query_userinfo.select('frindname','friendlink','firendimg','error')
    query_list_user = query_userinfo.find()


    # Result to arr
    api_json = {}
    friends_num = len(query_list_user)
    active_num = len(set([item.get('author') for item in query_list]))
    error_num = len([friend for friend in query_list_user if friend.get('error') == 'true'])
    acticle_num = len(query_list)
    last_updated_time = max([item.get('createdAt').strftime('%Y-%m-%d %H:%M:%S') for item in query_list])
    
    api_json['statistical_data'] = {
        'friends_num': friends_num,
        'active_num': active_num,
        'error_num': error_num,
        'acticle_num': acticle_num,
        'last_updated_time': last_updated_time
    }
    
    acticle_data = []
    for item in query_list:
        itemlist = {}
        for elem in list:
            itemlist[elem] = item.get(elem)
        acticle_data.append(itemlist)
    api_json['acticle_data'] = acticle_data
    
    with open("api.json", "w", encoding="utf-8") as api:
        api.write(json.dumps(api_json, indent=2, separators=(',', ':'), ensure_ascii=False))

    return api_json
    # Api handler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = getdata()
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        return
print(getdata())