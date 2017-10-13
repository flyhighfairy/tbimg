# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
import tbimg.settings as settings
import urllib.request
from PIL import Image


class TbimgPipeline(object):
    def process_item(self, item, spider):

        dir_path = '%s/%s' % (settings.IMAGES_STORE, item['category'])#存储路径

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for image_url in item['image_urls']:
            list_name = image_url.split('/')
            file_name = list_name[-1].replace("_300x300.jpg", "")#图片名称
            file_path = '%s/%s'%(dir_path, file_name)
            if os.path.exists(file_name):
                continue

            urllib.request.urlretrieve(image_url, file_path)
            img = Image.open(file_path)
            out = img.resize((299, 299), Image.ANTIALIAS)  # resize image with high-quality
            out.save(file_path)

        return item
