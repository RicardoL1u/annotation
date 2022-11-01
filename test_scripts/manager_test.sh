# manager login with passage and id
# id is phone
curl -X POST http://127.0.0.1:5000/manager/login -c manager.cookies -H 'Content-Type: application/json' -d '{"id":"110","token":"password"}'

# get all annotators who belongs to this manager
curl -X POST http://127.0.0.1:5000/manager/get_annotators -b manager.cookies

# assign task to one given annotator
# passage_start_idx is start index of passage
# passage_end_idx is end index of passage
curl -X POST http://127.0.0.1:5000/manager/assign_task -b manager.cookies  -H 'Content-Type: application/json' -d '{"annotator_id":"156","passage_start_idx":11,"passage_end_idx":13}'

# manager logout
curl -X POST http://127.0.0.1:5000/manager/logout -b manager.cookies