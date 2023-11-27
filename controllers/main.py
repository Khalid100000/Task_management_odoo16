from odoo import http 
from odoo.http import request
import re
import json
from urllib.request import urlopen
import requests

class MyPage(http.Controller):
    @http.route('/task',auth='public',website=True)
    def index(self,**kwargs):
        task=http.request.env['task.management.task'].search([])
        return  http.request.render(
            'task_management.index',{'tasks':task}
        )
    
    @http.route('/',auth='public',website=True)
    def main(self,**kwargs):
        forwarded_for = request.httprequest.headers.get('X-Forwarded-For')
        print(f'forwarded_for: {forwarded_for}')
        real_ip = forwarded_for.split(',')[0] if forwarded_for else request.httprequest.remote_addr
        print(f'remote_addr : {request.httprequest.remote_addr}')
        print('real_ip: ',real_ip)
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        output=[f'IP : {forwarded_for}']
        response = requests.get(f'http://ipinfo.io/{forwarded_for}/json')
        data = response.json()
        print(data)

        if 'country' in data:
            cnt = data['country']
            print(f'The IP address {forwarded_for} is located in {cnt}.')
            for k in data.keys():
                print(k)
                value=data[k]
                key=k.upper()
                if k not in ['readme','ip']:
                    output.append(f'{k} : {value}')
        else:
            print('Unable to retrieve country information.')
            output.append("Couldn't Recognize IP")

        return  http.request.render(
            'task_management.main',{'output':output}
        )

    @http.route('/task/<model("task.management.task"):task>/',auth='public',website=True)
    def task_detail(self,task):
        return http.request.render(
            'task_management.task_detail',{'task':task}
        )
    