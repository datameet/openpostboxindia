#!/usr/bin/env python
# coding=utf-8
import sys
import sqlite3 as lite
import requests
import time
from BeautifulSoup import BeautifulSoup
import dataset
import time
import datetime
import csv
import json
import urllib

db = dataset.connect('sqlite:///./postbox.sqlite')
post_box = db['post_box']
username = "odk-pradeep"
provider = "ODK_LOAD2"
row_one_done = False 
created_time = 1422204410
with open('OpenPostBoxIndia_results.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        if not row_one_done:
            row_one_done = True
            continue
        insert_record = {}
        post_id = row[0]
        post_id = post_id[5:]
        exists = post_box.find_one(post_id=post_id)
        if exists:
            print "Exists ="+(post_id )
            print "==========================================================================="
            continue
        else:
            pass
            
        insert_record['post_id']=post_id
        lat = row[2]
        lan = row[3]
        insert_record['lat']=lat
        insert_record['lan']=lan
        pincode = row[6]
        insert_record['pincode']=pincode

        type = row[7]
        insert_record['tags']=type
        
        address_url ="http://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","+lan+"&sensor=false&region=in"
        print address_url
        p = requests.get(address_url)
        jsons = json.loads(p.content)
        road = ""
        locality = ""
        district = ""
        state = ""
        formatted_address  = ""
        for results in jsons['results']:
            for address_components in results['address_components']:
                if "route" in address_components['types']:
                    road =address_components['long_name']
                if "locality" in address_components['types']:
                    locality =address_components['long_name']
                if "administrative_area_level_2" in address_components['types'] :
                    district =address_components['long_name']
                if "administrative_area_level_1" in address_components['types']:
                    state =address_components['long_name']                    
            formatted_address = results['formatted_address']
            break
        
        insert_record['picture_url'] = 'http://openbangalore.org/postboximg/'+post_id+'.jpg'
        insert_record['road']=road
        insert_record['locality']=locality
        insert_record['state']=state
        insert_record['district']=district
        insert_record['formatted_address']=formatted_address
        insert_record['caption']=road+", "+locality
        insert_record['provider']=provider
        insert_record['created_time']=created_time
        insert_record['username']=username

        
        outputFile = '/media/thej/data2/openpostboxindia/code/postboximg/'+post_id+'.jpg'
        urllib.urlretrieve(row[1], outputFile)
        post_box.insert(insert_record)
        db.commit()
        print str(insert_record)                
        #break


