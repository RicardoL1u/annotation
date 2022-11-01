curl -X POST http://127.0.0.1:5000/annotator/login -c annotator.cookies -H 'Content-Type: application/json' -d '{"id":"156","token":"password"}'

# curl -X POST http://127.0.0.1:5000/annotaotor/get_annotators -b annotator.cookies

# curl -X POST http://127.0.0.1:5000/annotator/assign_task -b annotator.cookies  -H 'Content-Type: application/json' -d '{"annotator_phone":"156","task_start_idx":11,"task_end_idx":13}'

curl -X GET http://127.0.0.1:5000/data/pageID=13 -b annotator.cookies

curl -X POST http://127.0.0.1:5000/data/pageID=13 -b annotator.cookies -H 'Content-Type: application/json' -d '{"data":{"id":"156","token":"password"}}'

curl -X POST http://127.0.0.1:5000/annotator/logout -b annotator.cookies