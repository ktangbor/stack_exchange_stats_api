## Requirement
The only hard requirement to run the project is to have the docker app installed and running.

## How to run
To run the project just execute "docker-compose up -d --build" (inside the StatAPI folder). 

## How to call
The calls can be made with the most ease through the Postman app. Of course, other methods like curl in cmd are valid. 
An example call is the url 
```
http://localhost:5000/api/v1/stackstats?since=2023-01-05 12:00:00&until=2023-04-30 13:00:05
```

which will return (in Postman): 
```json
"data": {
        "total_accepted_answers": 23,
        "accepted_answers_average_score": 5.35,
        "average_answers_per_question": 1.0,
        "top_ten_answers_comment_count": {
            "76095392": 2,
            "75464429": 4,
            "75504865": 3,
            "75570439": 3,
            "75195784": 1,
            "75283533": 0,
            "75307288": 0,
            "75837981": 0,
            "75578911": 1,
            "75747284": 0
        }
    }
```

## API Logic
The main app is the 'stat_drf' package. 
The package 'core' contains the logic and the main endpoint. 
In short, the api logic follows these steps
+ get from the url a 'from' and 'to' date parameter
+ use those params to get all the answers from the stack exchange api for that time period, 
and store them to the database (sqlit3).
+ get all comments for the above answers, and store them to the database
+ query the database to calculate the statistics
+ delete the data from the database

## Important notes 
- For the sake of this project, we receive only one page of results with the maximum 
allowed number of results (pagesize = 100) 
- Each call is assigned an api_call_id value (kind like a group id), in order to query and delete 
the data without risking including data from other parallel calls.
- This DRF api uses caching (memcached) on the results of each api call (per-view caching). 
The cache timeout is set to 15 minutes.
- The handling of exceptions has been kept at a minimum

## Unit testing
A directory has been created inside the main app called 'tests', where test can be created.

A sample test for the main view has been included, which tests if the main call returns status 200 (success).

To perform all the tests, execute 'python manage.py test' in StatAPI/api container's terminal (in the Docker app).
