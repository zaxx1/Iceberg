import os
import sys
import random
import string
import requests
import time
import json
from datetime import datetime, timedelta
import requests

class Iceberg:
    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://0xiceberg.com/webapp/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99", "Microsoft Edge WebView2";v="124"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
    
    def print_(self, word):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"[{now}] | {word}")

    def make_request(self, method, url, headers=None, json=None, data=None, params=None):
        retry_count = 0
        while True:
            time.sleep(2)
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, json=json)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=json, data=data, params=params)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=json, data=data)
            elif method.upper() == "PATCH":
                response = requests.patch(url, headers=headers, json=json)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, json=json)
            else:
                raise ValueError("Invalid method.")
            
            if response.status_code >= 500:
                if retry_count >= 4:
                    self.print_(f"Status Code: {response.status_code} | {response.text}")
                    return None
                retry_count += 1
            elif response.status_code >= 400:
                self.print_(f"Status Code: {response.status_code} | {response.text}")
                return None
            elif response.status_code >= 200:
                return response
    
    def current_user(self, query):
        url = 'https://0xiceberg.com/api/v1/users/user/current-user/'
        headers = {
            **self.headers,
            'x-telegram-auth': query
        }
        response = self.make_request('get', url, headers)
        if response is not None:
            res = response.json()
            return res
    
    def get_balance(self, query):
        url = 'https://0xiceberg.com/api/v1/web-app/balance/'
        headers = {
            **self.headers,
            'x-telegram-auth': query
        }
        response = self.make_request('get', url, headers)
        if response is not None:
            res = response.json()
            return res

    def collect(self, query):
        url = 'https://0xiceberg.com/api/v1/web-app/farming/collect/'
        headers = {
            **self.headers,
            'x-telegram-auth': query
        }

        response = self.make_request('delete', url, headers)
        if response is not None:
            res = response.json()
            return res
    
    def start(self, query):
        url = 'https://0xiceberg.com/api/v1/web-app/farming/'
        headers = {
            **self.headers,
            'x-telegram-auth': query
        }
        response = self.make_request('post', url, headers)
        if response is not None:
            res = response.json()
            return res
    
    def list_task(self, query):
        url = 'https://0xiceberg.com/api/v1/web-app/tasks/'
        headers = {
            **self.headers,
            'x-telegram-auth': query
        }
        response = self.make_request('get', url, headers)
        if response is not None:
            res = response.json()
            for item in res:
                id = item.get('id')
                status = item.get('status')
                price = item.get('price')
                description = item.get('description')
                data = {'id': id, 'price': price, 'desc': description}
                if 'plus' in description.lower():
                    continue
                if 'invite' in description.lower():
                    continue
                if 'subscribe' in description.lower():
                    continue
                if status == 'new':
                    self.start_task(query, data)
                elif status == 'ready_collect':
                    self.collect_task(query, data)
                else:
                    self.print_(f"Task {description} is Done")

    
    def start_task(self, query, data):
        id = data.get('id')
        url = f'https://0xiceberg.com/api/v1/web-app/tasks/task/{id}/'
        headers = {
            **self.headers,
            'x-telegram-auth': query
        }
        payload = {"status":"in_work"}
        response = self.make_request('patch', url, headers, payload)
        if response is not None:
            res = response.json()
            success = res.get('success', False)
            if success:
                desc = data.get('desc')
                self.print_(f"Task id {desc} Started")
                time.sleep(3)
                self.verify_task(query, data)
    
    def verify_task(self, query, data):
        id = data.get('id')
        url = f'https://0xiceberg.com/api/v1/web-app/tasks/task/{id}/'
        headers = {
            **self.headers,
            'x-telegram-auth': query
        }
        payload = {"status":"ready_collect"}
        response = self.make_request('patch', url, headers, payload)
        if response is not None:
            res = response.json()
            success = res.get('success', False)
            if success:
                desc = data.get('desc')
                self.print_(f"Task id {desc} Verified")
                self.collect_task(query, data)
    
    def collect_task(self, query, data):
        id = data.get('id')
        url = f'https://0xiceberg.com/api/v1/web-app/tasks/task/{id}/'
        headers = {
            **self.headers,
            'x-telegram-auth': query
        }
        payload = {"status":"collected"}
        response = self.make_request('patch', url, headers, payload)
        if response is not None:
            res = response.json()
            success = res.get('success', False)
            if success:
                desc = data.get('desc')
                self.print_(f"Task id {desc} Done")
    
    def show_ads(self, id, premium):
        url = f"https://api.adsgram.ai/adv?blockId=3721&tg_id={id}&tg_platform=android&platform=Win32&language=en&is_premium={premium}&top_domain=0xiceberg.com"
        headers = {
            **self.headers
        }
        response = self.make_request('patch', url, headers)
        if response is not None:
            res = response.json()
            campaignId = res.get('campaignId')
            bannerId = res.get('bannerId')
            self.print_(f"Done {campaignId} {bannerId}")