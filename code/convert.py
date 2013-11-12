import sqlite3
import json

conn = sqlite3.connect("/home/thej/Desktop/postbox.sqlite") # or use :memory: to put it in RAM
cursor = conn.cursor()
 #go to pincode table
results = cursor.execute("""select pincode from pin_code order by pincode """)


#get a single pinocode
for row in results:
	geojson = {}
	geojson["type"] = "FeatureCollection"
	features = []

	code = row[0]
	cursor2 = conn.cursor()
	post_boxes = cursor2.execute("""select * from post_box where pincode='"""+code+"""' order by created_time """)
	for box in post_boxes:
		data = {}
		data["ID"]=box[0]
		data["IMG"]=box[1]
		data["TAGS"]=box[2]
		data["CONTRIBUTOR"]=box[6]
		data["PINCODE"]=box[8]
		data["CAPTION"]=box[9]
		data["DISTRICT"]=box[13]
		data["STATE"]=box[14]		
		data["ADDRESS"]=box[15]
		data["HOMEPAGE"]='http://openbangalore.org/postbox/pb/id/'+data['ID']
		single_feature = {}
		single_feature['geometry']={"type":"Point","coordinates":[float(box[4]), float(box[3])]}
		single_feature['properties']=data
		single_feature["type"]= "Feature"
		features.append(single_feature)
	geojson["features"]=features
	json_data = json.dumps(geojson, indent=4, sort_keys=True)
	file_name = "../pincode/pin_"+code+".geojson"
	f = open(file_name, 'w')
	f.write(json_data)


#provide API
#http://gitspatial.com/api/v1/
