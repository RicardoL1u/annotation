import sqlite3
import datetime
import json
conn = sqlite3.connect('database.db')
print( "Opened database successfully")


# MANAGER_ID = '15933111848' # AISHU
# output_file_name = 'aishu.json'
MANAGER_ID = '17392323793' # LONGMAO
output_file_name = 'longmao.json'



annotator_ids = [id[0] for id in conn.execute(f"SELECT id from annotator where manager_id={MANAGER_ID}")]
print(f'there are {len(annotator_ids)} annotators employed')
cmd = "SELECT annotated_filename,passage_ori_id,create_timestamp from annotated_data where " + \
    " or ".join([f"annotator_id=\"{id}\"" for id in annotator_ids])
annotated_datas = [[filename,passage_ori_id,datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')] for filename,passage_ori_id,timestamp in conn.execute(cmd) ]
print(f'there are {len(annotated_datas)} data')
annotated_datas.sort(key=lambda x:(x[1],x[2]))
passage_results = {data[1]:data[0] for data in annotated_datas}
print(f'there are {len(passage_results)} passages')
with open(output_file_name,'w') as f:
    json.dump(passage_results,f,indent=4)

print( "Operation done successfully")
conn.close()