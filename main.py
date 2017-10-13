#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/28 10:14
# @Author  : Fairy Huang
# @File    : main.py
# @Project: LabCrawler

from scrapy.cmdline import execute

execute(["scrapy", "crawl", "tbimg_spider"])