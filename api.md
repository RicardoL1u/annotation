# Annotator
## Annotator Login
| URL                            | METHOD | Cookie | Tips |
| ------------------------------ | ------ | ------ | ---- |
| 127.0.0.1:5000/annotator/login | POST   | False  |      |

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
| 127.0.0.1:5000/data/pageID=idx | GET    | True   | Idx是一个数据点在整个数据集中的下标 |

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
| 127.0.0.1:5000/data/pageID=idx | POST   | False  | 注意和上一个api区分（上一个采用GET方法） |

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
  "code":0
}
```

## Annotator Logout
| URL                            | METHOD | Cookie | Tips |
| ------------------------------ | ------ | ------ | ---- |
| 127.0.0.1:5000/annotator/logout | POST   | True  |      |

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
| 127.0.0.1:5000/manager/login | POST   | False  |      |

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
| 127.0.0.1:5000/manager/logout | POST   | True  |      |

**Request Body**
```json
```

**Return Info**

```json
```

## Manager Get Annotators

| URL                                   | METHOD | Cookie | Tips |
| ------------------------------------- | ------ | ------ | ---- |
| 127.0.0.1:5000/manager/get_annotators | POST   | True   |      |

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
| 127.0.0.1:5000/manager/assign_task | POST   | True   |      |

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