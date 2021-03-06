# -*- coding: utf-8 -*-
"""
@description: 
@author:XuMing
"""
from __future__ import print_function  # 兼容python3的print写法
from __future__ import unicode_literals  # 兼容python3的编码处理

import json
import os
import urllib
import urllib2


def cosplay(member_id, page=1, index=0):
    url = 'http://worldcosplay.net/en/api/member/photos?member_id=%s&page=%s&limit=100000&rows=16&p3_photo_list=1' % (
        member_id, page)
    r = urllib2.urlopen(url)

    if r.code == 200:
        data = json.loads(r.read())
        if data['has_error'] != 0:
            print(u'接口挫了')
            exit(1)

        photo_data_list = data['list']
        if not photo_data_list:
            print(u'没东西了？第 %s 页，共下载了 %s 个图片' % (page, index - 1))
            exit(0)
        for photo_data in photo_data_list:
            url = photo_data['photo']['sq300_url']
            subject = photo_data['photo']['subject']
            url = url.replace('/sq300', '')
            subject = subject.replace('/', '_')

            if not os.path.exists(member_id):
                os.makedirs(member_id)

            filename = '%s/%s_%s_%s.jpg' % (member_id, member_id, index, subject)
            try:
                urllib.urlretrieve(url=url, filename=filename)
                print(u'下完了%s张' % (index + 1))
                index += 1
            except Exception:
                print(u'这张图片下载出问题了： %s' % url)

        page += 1
        cosplay(member_id, page=page, index=index)

    else:
        print(u'挫了')
        exit(1)


if __name__ == '__main__':
    member_id = raw_input("请输入coser ID，例如：53056:") // 51079, 53051
    if len(member_id) < 2:
        exit(1)
    cosplay(member_id)
