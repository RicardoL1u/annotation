# manager login with passage and id
# id is phone
curl -X POST http://103.238.162.37:9494/manager/login -c manager.cookies -H 'Content-Type: application/json' -d '{"id":"110","token":"password"}'


# curl -X POST http://103.238.162.37:9494/manager/sign_up_annotator -b manager.cookies -H 'Content-Type: application/json' -d '{"annotator_id":"15673309902","annotator_name":"yantao","annotator_token":"password"}'


# get all annotators who belongs to this manager
# curl -X POST http://103.238.162.37:9494/manager/get_annotators -b manager.cookies

# assign task to one given annotator
# passage_start_idx is start index of passage
# passage_end_idx is end index of passage
# curl -X POST http://103.238.162.37:9494/manager/assign_task -b manager.cookies  -H 'Content-Type: application/json' -d '{"annotator_id":"156","passage_start_idx":1,"passage_end_idx":150}'

# curl -X POST http://103.238.162.37:9494/manager/get_task_list -b manager.cookies

# curl -X POST http://103.238.162.37:9494/manager/review_task -b manager.cookies -H 'Content-Type: application/json' -d '{"annotator_id":"156","task_id":1}'

# curl -X POST http://103.238.162.37:9494/manager/get_task_list -b manager.cookies

# curl -X POST http://103.238.162.37:9494/manager/review_one_data_point -b manager.cookies -H 'Content-Type: application/json' -d '{"annotated_filename":"80d69f45a35caa22011ae3c9290f9cafbe475f2ba5057ad3eaea7c8cb425f044.json"}'
curl -X POST http://103.238.162.37:9494/data/download -b manager.cookies --output test.zip


# manager logout
curl -X POST http://103.238.162.37:9494/manager/logout -b manager.cookies