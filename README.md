# Annoy QA annotation platform

## How To Run
1. apt install sqlite3
2. pip install -r requirments.txt
3. bash run.sh

## 一些测试数据

1. **可以用来测试登录的manager**
   
    ```bash
    curl -X POST http://127.0.0.1:5000/manager/login -c manager.cookies -H 'Content-Type: application/json' -d '{"id":"110","token":"password"}'
    ```
    > 和之前约定不同的是，这里的id是一个string，而不是int，其实就是手机号
    >
    > 这里的 -c manager.cookies 是用来设置cookies的，把cookie存到managers.cookies 这个文件当中
    >
    > 这里的 -X 代表使用的方法是 POST （一般来说，

2. 可以用来测试登陆的annotator

    ```bash
    curl -X POST http://127.0.0.1:5000/annotator/login -c annotator.cookies -H 'Content-Type: application/json' -d '{"id":"156","token":"password"}'
    ```
    > 和之前约定不同的是，这里的id是一个string，而不是int，其实就是手机号

3. 在保持manager的登陆态（也就是cookie）我们可以拉取 属于这个 manager 手下的 全部 annotator
    ```bash
    curl -X POST http://127.0.0.1:5000/manager/get_annotators -b manager.cookies
    ```

4. 在保持manager的登陆态（也就是cookie），我们assign task 给 id为156 的annotator

    ```bash
    curl -X POST http://127.0.0.1:5000/manager/assign_task -b manager.cookies  -H 'Content-Type: application/json' -d '{"annotator_id":"156","passage_start_idx":11,"passage_end_idx":13}'
    ```
    > 这里的 -b manager.cookies 是用来使用之前 login 时 用 -c manager.cookies 生成的cookie文件
    >
    > passage_start_idx 是你想要分配过去的第一篇文章
    >
    > passage_end_idx 是你想要分配过去的最后一篇文章


5. 在保持annotator的登陆态（也就是cookie），我们标注可以标注文章 

    ```bash
    curl -X GET http://127.0.0.1:5000/data/pageID=13 -b annotator.cookies
    ```
    > 这里是 -X GET 表示使用GET方法，这里会拉取一个需要标注的数据点

    ```bash
    curl -X POST http://127.0.0.1:5000/data/pageID=13 -b annotator.cookies -H 'Content-Type: application/json' -d '{"data":{"id":"156","token":"password"}}'
    ```
    > 通过 -X POST 使用POST方法，回传标注结果
    >
    > "data"： 之后的字典就是标注结果 -- 样例中的 字典内容只用来测试，不是真正的标注结果

 