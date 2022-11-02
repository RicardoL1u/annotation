curl -X POST http://103.238.162.37:9522/annotator/login -c annotator.cookies -H 'Content-Type: application/json' -d '{"id":"156","token":"password"}'

# get the data of 13th passage
# the return data format is 
# dataset[idx] follow the format we argee at 34:/data/lyt/workspace/Seq2Seq-MRC/analysis/company_dataformat.md 
        # return {
        #     'message': "data",
        #     'data':dataset[idx],
        #     'code': 1
        # }

# curl -X GET http://103.238.162.37:9522/data/pageID=13 -b annotator.cookies

# "data" contain the annotated result of 13th passage
curl -X POST http://103.238.162.37:9522/data/pageID=13 -b annotator.cookies -H 'Content-Type: application/json' -d '{"data":{"id":"156","token":"password"}}'
curl -X POST http://103.238.162.37:9522/annotator/get_task_list -b annotator.cookies
#
curl -X POST http://103.238.162.37:9522/annotator/logout -b annotator.cookies