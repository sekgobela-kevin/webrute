# webrute
Webrute is python bruteforce library for bruteforcing websites. It can 
be used to check if certain url works with certain parameters or data
passed to it. It is based on 
[broote](https://github.com/sekgobela-kevin/broote) which also does
bruteforcing but not limited to websites and web requests.

Webrute is so similar to 'broote' but it offers opportunity to perform
web requests. It is currencly using 
[requests](https://requests.readthedocs.io/projects/requests-html/en/latest/)
and [aiohttp](https://docs.aiohttp.org/en/stable/client_quickstart.html)
for performing requests.

> See [broote](https://github.com/sekgobela-kevin/broote) for more.

### Install
This is enough to install 'webrute' in your commnd-line application.
```bash
pip install webrute
```

### Usage
Data for bruteforce need to be prepared first before getting started.
```python
import asyncio


passwords_field = webrute.field("password", lambda: range(10))
usernames_field = webrute.field(["Ben", "Jackson", "Marry"])

table = webrute.table()
table.add_field(passwords_field)
table.add_primary_field(usernames_field)
```

Target in webrute can be 'str' which will be taken as url or 'dict' with 
information for request.  
Record will be used together with target which will then be sent as part
of request.

This code sample shows target and record with final 'dict' that will be 
used as part of request.  

Keys used in target or record are same as arguments used for performing request with
[requests](https://requests.readthedocs.io/projects/requests-html/en/latest/)
library.

```python
target = {"url": "https://example.com/login", "method": "POST"}
request = {"data": {"username": "Marry", "password": 10}}

request_info = {
    "url": "https://example.com/", "method": "POST",  "data": {
        "username": "Marry", "password": 10}
}
```

Its best to have target hold only information that wont change and let record
hold information that may change like 'password'.  

> Basics of [broote](https://github.com/sekgobela-kevin/broote) are 
required to continue.


The most difficult function to define is `connect()` which is 
the one performing request into target. Connector provides 'target',
'record' and 'session' which are enough to perform request.

Webrute already provide connector function which will perform the 
actual request. This is best to ensure that to transform record
into format for performing request.
```python
import webrute

def connector(target, record, session=None):
    # Creates new record containing 'data' field.
    new_record = webrute.record()
    new_record.add_item("data", dict(record))
    # webrute.connector() performs request and return response.
    return webrute.connector(target, new_record, session)
```
> Session is set by default which is shared by all requests.  

Connector is now combined with `success()`, `failute()` and `target()` 
functions.
```python
import webroote

def connector(target, record, session=None):
    # Creates new record containing 'data' field.
    new_record = webrute.record()
    new_record.add_item("data", dict(record))
    # webrute.connector() performs request and return response.
    return webrute.connector(target, new_record, session)

def success(response):
    return b"logged in as " in response.read()

def failure(response):
    return b"Username and password does not match" in response.read()

def target_reached(response):
    # This is current implementation of defaut target reached.
    # return webrute.target_reached(response)
    return response.get_status_code() == 200
```

> Target reached by default is True when status code is 200.

Things now start to look exatly as in
[broote](https://github.com/sekgobela-kevin/broote) which also inclues 
creation of runner.  

Creating request can take some time if not executed in parallel or 
concurrently. Using `webrute.thread_runner` runner is best choice as it uses
threads for performing bruteforce.
```python
# Code for table is at top.
# ... ... ... ... ... ... .

def connector(target, record, session=None):
    # Creates new record containing 'data' field.
    new_record = webrute.record()
    new_record.add_item("data", dict(record))
    # webrute.connector() performs request and return response.
    return webrute.connector(target, new_record, session)

def success(response):
    return b"logged in as " in response.read()

def failure(response):
    return b"Username and password does not match" in response.read()

def target_reached(response):
    # This is current implementation of defaut target reached.
    # return webrute.target_reached(response)
    return response.get_status_code() == 200


# Creates runner executing in multiple threads.
target = {"url": "https://example.com/login", "method": "POST"}
runner = broote.thread_runner(target, table, connect=connect_webpage,success=success, failure=failure, target_reached=target_reached)

# Starts requests using connector()
runner.start()
runner.get_success_records() # [{'username': 'Marry', 'password': 8}]
```
> [https://example.com/login](https://example.com/login) does not exists as used in above example.


`webrute.async_runner` runner is also useful but uses asyncio to perfom
request using 
[aiohttp](https://docs.aiohttp.org/en/stable/client_quickstart.html)
library.
```python
# Code for table is at top.
# ... ... ... ... ... ... .

async def connector(target, record, session=None):
    # Creates new record containing 'data' field.
    new_record = webrute.record()
    new_record.add_item("data", dict(record))
    # webrute.connector() performs request and return response.
    return await webrute.async_connector(target, new_record, session)

async def success(response):
    return b"logged in as " in await response.read()

async def failure(response):
    return b"Username and password does not match" in await response.read()

async def target_reached(response):
    # This is current implementation of defaut target reached.
    # return webrute.target_reached(response)
    return response.get_status_code() == 200


# Creates runner executing using asyncio
target = {"url": "https://example.com/login", "method": "POST"}
runner = broote.async_runner(target, table, connect=connect_webpage,success=success, failure=failure, target_reached=target_reached)

# Starts requests using connector()
# asyncio.run(runner.astart())
runner.start()
runner.get_success_records() # [{'username': 'Marry', 'password': 8}]
```

> More features are available through 'broote' library.


### Progress and Issues
- 'webrute' is currently unstable and not guaranteed to work.
- Not having automated tests means there are lot of bugs.
- Undefined goals and requirements led to poor implementation.
- 'webrute' code can be easily be replaced with 'broote' with ease.


### License
Webrute is released as open-source under conditions of 
[GPL-3.0](https://github.com/sekgobela-kevin/webrute/blob/main/LICENSE)
license.