import sqlite3
import datetime
import json
conn = sqlite3.connect('database.db')
print( "Opened database successfully")


MANAGER_ID = '15933111848' # AISHU
# MANAGER_ID = '17392323793' # LONGMAO


annotator_ids = [id[0] for id in conn.execute(f"SELECT id from annotator where manager_id={MANAGER_ID}")]
cmd = "SELECT annotated_filename,passage_ori_id,create_timestamp from annotated_data where " + \
    " or ".join([f"annotator_id=\"{id}\"" for id in annotator_ids])
annotated_datas = [[filename,passage_ori_id,datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')] for filename,passage_ori_id,timestamp in conn.execute(cmd) ]

annotated_datas.sort(key=lambda x:(x[1],x[2]))
passage_results = {data[1]:data[0] for data in annotated_datas}

with open('aishu.json','w') as f:
    json.dump(passage_results,f,indent=4)

print( "Operation done successfully")
conn.close()