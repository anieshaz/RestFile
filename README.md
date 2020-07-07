# RESTFul data subscriber

> Subscribe data from a delimited file using REST api

---

## Usage

- Define the param.yaml file ex:

 ```yaml
 # Port Number
port : 5000
# Input file path
filename : '/home/data.out'
# Delimiter
delimiter : '|'
# Filtering key column
keyColumn : 'ID'
# Output Columns
outColumns:
  - ID
  - NAME
  ```
  
- The input file can be any delimited file with any number of columns

  ```csv
  ID|NAME|DEPT
  1|John|20
  2|Paul|30
  3|George|70
  3|Ringo|60
  ```


- Run the application

  ```python
  python main.py
  ```

- Subscribe the data

    ```curl
    curl -X GET http://INW1PF1AQDMR:99/api/get/1

    {
        "ID": 1,
        "NAME": 'Animesh',
        "DEPT": '10'
    }
    ````

---

## Logging

- Check the logs in case of any errors
- Log is created in the working directory with the name of **"run-app.log"**
```log
2020-07-07 12:29:20,219 :: INFO :: Parameter file paramTest.yaml read successfully
2020-07-07 12:29:20,219 :: INFO :: Fetching Parameters from paramTest.yaml
2020-07-07 12:29:20,222 :: INFO :: Syntax check for test.dat passed sucessfully
2020-07-07 12:29:20,316 :: INFO ::  * Running on http://HOSTANIEPC:8000/ (Press CTRL+C to quit)
```

---

## Common Errors

- Bad request (400) : Only get is supported as of now
- Bad url (404) : Check logs to get the suggested URL
- No Data : If there is no data for the provided filter in the URL

---

## Author Details

Animesh Srivastava  | postanisrivastava@outlook.com  

[![Linkedin](https://i.stack.imgur.com/gVE0j.png) LinkedIn](https://www.linkedin.com/in/animesh-srivastava-12390a107/)
&nbsp;
[![GitHub](https://i.stack.imgur.com/tskMh.png) GitHub](https://github.com/anieshaz)
