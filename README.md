## Gogolook Interview Coding Exercise
 - It's a task Restful API server

### How to Activate
```bash
docker-compose up -d
```

### How to deactivate
```bash
docker-compose down
```

### API Document
#### 1.  GET /tasks (list tasks)
```
{
    "result": [
        {"id": 1, "name": "name", "status": 0}
    ]
}
```

#### 2.  POST /task  (create task)
```
request
{
  "name": "買晚餐"
}

response status code 201
{
    "result": {"name": "買晚餐", "status": 0, "id": 1}
}
```

#### 3. PUT /task/<id> (update task)
```
request
{
  "name": "買早餐",
  "status": 1
  "id": 1
}

response status code 200
{
  "name": "買早餐",
  "status": 1,
  "id": 1
}
```

#### 4. DELETE /task/<id> (delete task)
response status code 200


### Who do I talk to?
* Author: Howard Chen (howard5248@gmail.com)