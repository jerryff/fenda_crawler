# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os.path
import pandas as pd
from config import FileConfig
from scrapy.exceptions import DropItem
import csv

class LivePipeline(object):
    def __init__(self):
        self.live_data = None
        self.comment_folder = "comments/"
        self.doctor_list=[]
        self.csvfile=None

    def open_spider(self, spider):
        # self.live_outfile = open(FileConfig["name"], "r")
        # self.live_data = pd.DataFrame(json.loads(line) for line in self.live_outfile)
        # self.live_outfile.close()

        # self.live_outfile = open(FileConfig["name"], "a")
        self.csvfile = open(FileConfig["name"],'wb')
        self.live_outfile = csv.writer(self.csvfile,dialect='excel')     

    def process_item(self, item, spider):
        if item["type"] == "speech":
            self.process_live_data(item)

        if item["type"] == "comment":
            self.process_comment_data(item)
        # print self.doctor_list
        

    def close_spider(self, spider):
        print self.doctor_list
        self.live_outfile.writerows(self.doctor_list)
        self.csvfile.close()
        # self.live_outfile.close()

    def process_live_data(self, item):
        pass
        # for each in item:
        #     if each["id"] in self.live_data.id.values:
        #         DropItem("live id %s already exists" % each["id"])
        #     else:
        #         self.live_outfile.writelines(json.dumps(each) + "\n")
        #         self.live_data = self.live_data.append(each, ignore_index = True)

    def process_comment_data(self, item):
        # if os.path.exists( self.comment_folder + item["id"]):
        #     comment_outfile = open( self.comment_folder + item["id"])
        #     comment_data = pd.DataFrame(json.loads(line) for line in comment_outfile)
        #     comment_outfile.close()

        #     comment_outfile = open( self.comment_folder + item["id"], "a")

        #     for each in item["data"]:
        #         if each["id"] in comment_data.id.values:
        #             DropItem("comment id %s already exists!" % each["id"])
        #         else:
        #             comment_outfile.writelines(json.dumps(each) + "\n")
        #             comment_data = comment_data.append(each, ignore_index=True)

        #     comment_outfile.close()

        # else:
        #     comment_outfile = open( self.comment_folder + item["id"], 'w')
        #     for each in item["data"]:
        #         comment_outfile.writelines(json.dumps(each) + "\n")
        #     comment_outfile.close()
        for items in item['data']:
            for i in items:
                data=[]
                # print i
                jr=json.loads(i)
                data.append(jr['leader']['nickname'])
                data.append(jr['leader']['title'])
                tag_id=[]
                tag_name=[]
                for j in jr['leader']['tags']:
                    tag_id=j['id']
                    tag_name=j['name']
                data.append(tag_id)
                data.append(tag_name)
                data.append(jr['leader']['introduction'])
                data.append(jr['leader']['price'])
                data.append(jr['leader']['answer_probability'])
                data.append(jr['leader']['answers_count'])
                data.append(jr['leader']['followers_count'])
            for i in range(len(data)):
                # print type(data[i]) 
                # print data[i]
                if isinstance(data[i],(unicode)):
                    # print data[i] 
                    data[i]=data[i].encode("gbk") 
                    # print data[i]
            self.doctor_list.append(data)

