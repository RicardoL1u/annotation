# Annotator
## Annotator Login
| URL                            | METHOD | Cookie | Tips |
| ------------------------------ | ------ | ------ | ---- |
| 103.238.162.37:9522/annotator/login | POST   | False  |      |

**Request Body**
```json
{
  "id":"phone number",
  "token":"password"
}
```

**Return Info**

```json
{
   "message": "Logged in successfully!",
   "code": 1,
},
{
    "message": "The token is invalid. Please try again.",
    "code": 0
},
{
    "message":"You are not authorized to view this page",
    "code":0
}
```

## Annotator Get one Data Point
| URL                            | METHOD | Cookie | Tips                                |
| ------------------------------ | ------ | ------ | ----------------------------------- |
| 103.238.162.37:9522/data/pageID=hasd_id | GET    | True   |  |

> 具体hash_id要从 37:/data/lyt/workspace/annotation/data/company_data.json 中获取

**Request Body**

```json
None
```

**Return Info**

```json
{
    "message": "data",
    "data":{}, // data这个字典里数据的格式可以参考 34:/data/lyt/workspace/Seq2Seq-MRC/analysis/company_dataformat.md
    "code": 1
}
```

## Annotator Submit Annotated Data
| URL                            | METHOD | Cookie | Tips                                     |
| ------------------------------ | ------ | ------ | ---------------------------------------- |
| 103.238.162.37:9522/data/pageID=idx | POST   | False  | 注意和上一个api区分（上一个采用GET方法） |

> 具体hash_id要从 37:/data/lyt/workspace/annotation/data/company_data.json 中获取
>
> 这里在最新的更新之后：不再需要通过assign task 来具体分配给 当前annotator 才能访问了，（访问限制通过hash id来实现）

**Request Body**

```json
{
  "data":{
    "passage_id":"passage_hashed_id",
    "context":"refined context",
    "annoymous_name": "xxx",
    "question_text_list":[
      {
        "question_id":"question_hashed_id",
        "question_text": "question_text"
      },....
    ]
  }
}
```

**Return Info**

```json
{
  "message":"Annotation Task Done!",
  "annotated_filename":"b69beecf1775563c976831aef3d03681684da796739b80d84ecbb18c416b098d.json",
  "code":0
}
```

## Annotator Get Task List

| URL                                         | METHOD | Cookie | Tips |
| ------------------------------------------- | ------ | ------ | ---- |
| 103.238.162.37:9522/annotator/get_task_list | POST   | True   |      |

**Request Body**

```json

```

**Return Info**

```json
{
  "message":"here is the task list",
  "task_list":[
    {
      "passage_id":passage_idx,
      "passage_title":"title",
      "task_done_number":task_done_number // integer, equal to 0 for have not done yet
    }
  ]
  "code":0
}
```



## Annotator Logout

| URL                            | METHOD | Cookie | Tips |
| ------------------------------ | ------ | ------ | ---- |
| 103.238.162.37:9522/annotator/logout | GET   | True  |      |

**Request Body**
```json
```

**Return Info**

```json
{
  "message":"You have successfully logged out",
  "code":0
}
```







# Manager

## Manager Login
| URL                          | METHOD | Cookie | Tips |
| ---------------------------- | ------ | ------ | ---- |
| 103.238.162.37:9522/manager/login | POST   | False  |      |

**Request Body**
```json
{
  "id":"phone number",
  "token":"password"
}
```

**Return Info**

```json
```

## Manager Logout
| URL                            | METHOD | Cookie | Tips |
| ------------------------------ | ------ | ------ | ---- |
| 103.238.162.37:9522/manager/logout | GET   | True  |      |

**Request Body**
```json
```

**Return Info**

```json
```

## Manager Get Annotators

| URL                                   | METHOD | Cookie | Tips |
| ------------------------------------- | ------ | ------ | ---- |
| 103.238.162.37:9522/manager/get_annotators | POST   | True   |      |

**Request Body**

```json

```

**Return Info**

```json
{
  "annotators": [
    {
      "id": "156", // id (aka the phone) of annotator
      "name": "liu", // annotator name
      "manager_id": 110
    }
  ], 
  "code": 1, 
  "message": "Annotators list"
}
```

## Manger Assign Task

| URL                                | METHOD | Cookie | Tips |
| ---------------------------------- | ------ | ------ | ---- |
| 103.238.162.37:9522/manager/assign_task | POST   | True   |      |

**Request Body**

```json
{
  "annotator_id":"phone number",
  "passage_start_idx":23,
  "passage_end_idx":32
}
```

**Return Info**

```json
{
    "message": f"Annotator {suc_cnt} task assigned successfully",
    "assigned_task_num": suc_cnt,
    "code": 1
}
```

这里有一个 suc_cnt 是因为 一篇文章只能被 assign 给一个 annotator 一次，如果第二次重复assign，就会失败，并跳过这一次assign

## Manger Get Task List

| URL                                       | METHOD | Cookie | Tips |
| ----------------------------------------- | ------ | ------ | ---- |
| 103.238.162.37:9522/manager/get_task_list | POST   | True   |      |

**Request Body**

```json

```

**Return Info**

```json
{
  "code": 1,
  "messages": "here is the task list of this manager",
  "task_list": [
    {
      "annotated_filename": null,
      "annotator_id": "156",
      "last_done_timestamp": "Thu, 03 Nov 2022 11:19:17 GMT",
      "passage_id": 11,
      "passage_ori_id": "df3d0e4eccad5b1c290d4714a1149a8b02d75bb4ae86db231194d03ab7df5b73",
      "task_done_number": 1,
      "task_id": 1,
      "task_status": 1
    },
  ]
}
```

Task_status == 0 表示这个task需要标注

Task_status == 1 表示这个task标注完成需要review

Task_status == 2 表示这个task - review完成并认同最新一次的结果

## Manger Get Review Task 

| URL                                       | METHOD | Cookie | Tips |
| ----------------------------------------- | ------ | ------ | ---- |
| 103.238.162.37:9522/manager/get_task_list | POST   | True   |      |

**Request Body**

```json
{
  "task_id":12,
  "task_status":1 // this could be none, 假如没有这个字段则会返回review 需要的信息
}
```

> 关于task status的说明详见 Manger Get Task List 这个api -> 这里是改变这个task_status 的值从而完成review的效果

**Return Info**

假如有 task_status 字段

```json
{
  "code": 1,
  "message": "task status successfully updated."
}
```

假如没有 task_status字段

```json
{
 "annotated_data": {
    "id": "156",
    "token": "password"
  },
  "code": 0,
  "message": "the last annotated data.",
  "passage": {},
}
```



>Task_status == 0 表示这个task需要标注
>
>Task_status == 1 表示这个task标注完成需要review
>
>Task_status == 2 表示这个task - review完成并认同最新一次的结果

## Manager Review One Data Point

| URL                                               | METHOD | Cookie | Tips |
| ------------------------------------------------- | ------ | ------ | ---- |
| 103.238.162.37:9522/manager/review_one_data_point | POST   | True   |      |

**Request Body**

```json
{
  "annotated_filename":"b69beecf1775563c976831aef3d03681684da796739b80d84ecbb18c416b098d.json",
  // 注意这个.json的后缀必不可少
}
```

**Return Info**

```json
{
        "annotated_data":json.load(open("data/"+annotated_filename)),
        "annotator_id": data.annotator_id,
        "create_timestamp":data.create_timestamp,
        "passage_ori_id":data.passage_ori_id,
        "code":1
}
```

## Manager Signup Annotator

| URL                                           | METHOD | Cookie | Tips |
| --------------------------------------------- | ------ | ------ | ---- |
| 103.238.162.37:9522/manager/sign_up_annotator | POST   | True   |      |

**Request Body**

```json
{
  "annotator_id":"phone number",
  "annotator_name": "name",
  "annotator_token":"password",
}
```

**Return Info**

```json
{
   "message": "Annotator has been successfully sign up",
   "code":0
}
```

这里有一个 suc_cnt 是因为 一篇文章只能被 assign 给一个 annotator 一次，如果第二次重复assign，就会失败，并跳过这一次assign

# Data

## Download

## Manager Signup Annotator

| URL                               | METHOD | Cookie | Tips |
| --------------------------------- | ------ | ------ | ---- |
| 103.238.162.37:9522/data/download | POST   | True   |      |

**Request Body**

```json

```

**Return Info**

```json

```

> 对于一个annotator 只会返还由他标注的所有数据
>
> 对于 manager 而言则会直接返还所有数据
>
> 是一个zip 文件


