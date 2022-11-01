curl -X POST http://127.0.0.1:5000/manager/login -c manager.cookies -H 'Content-Type: application/json' -d '{"phone":"110","token":"password"}'

curl -X POST http://127.0.0.1:5000/manager/get_annotators -b manager.cookies

curl -X POST http://127.0.0.1:5000/manager/assign_task -b manager.cookies  -H 'Content-Type: application/json' -d '{"annotator_phone":"156","task_start_idx":11,"task_end_idx":13}'

curl -X POST http://127.0.0.1:5000/manager/logout -b manager.cookies