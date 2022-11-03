# manager login with passage and id
# id is phone
curl -X POST http://103.238.162.37:9494/manager/login -c manager.cookies -H 'Content-Type: application/json' -d '{"id":"110","token":"password"}'


# curl -X POST http://103.238.162.37:9494/manager/sign_up_annotator -b manager.cookies -H 'Content-Type: application/json' -d '{"annotator_id":"15673309902","annotator_name":"yantao","annotator_token":"password"}'


# get all annotators who belongs to this manager
curl -X POST http://103.238.162.37:9494/manager/get_annotators -b manager.cookies

# assign task to one given annotator
# passage_start_idx is start index of passage
# passage_end_idx is end index of passage
curl -X POST http://103.238.162.37:9494/manager/assign_task -b manager.cookies  -H 'Content-Type: application/json' -d '{"annotator_id":"156","passage_start_idx":11,"passage_end_idx":13}'

curl -X POST http://103.238.162.37:9494/manager/get_task_list -b manager.cookies


# manager logout
curl -X POST http://103.238.162.37:9494/manager/logout -b manager.cookies