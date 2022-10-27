# webrute
Webrute is python bruteforce library for http requests built on top of
[broote](https://github.com/sekgobela-kevin/broote).  It can be used 
for bruteforce activities involving making https requests including 
checking status code for request with certain data passed.

Requests are performed using [httpx](https://www.python-httpx.org/) which
support [asyncio](https://docs.python.org/3/library/asyncio.html).

> See [broote](https://github.com/sekgobela-kevin/broote) for more.
### Install
This is enough to install 'webrute' in your command-line application.
```bash
pip install webrute
```

### Usage
Data for bruteforce need to be prepared first before getting started.
```python
import webrute

passwords_field = webrute.field("password", lambda: range(10))
usernames_field = webrute.field("username", ["Ben", "Jackson", "Marry"])

table = webrute.table()
table.add_field(passwords_field)
table.add_primary_field(usernames_field)
```

**Target** in 'broote' defines anything that can be used to interact with
system to be bruteforced. Here in webrute, _str_ target will be considered url or but _dict_ can be provided with information defining target.

_dict_ as target will have to contain keywords arguments for request 
including 'url', 'method', etc. Record can also provide arguments for 
request just like target does.

Here is how target and record as _dict_ can be used to create arguments
to be used in request.
```python
# target_dict contain basic information for making request.
target_dict = {"url": "https://example.com/login", "method": "POST"}
# record_dict provides extra information.
# record_dict was created from table record as seen.
record_dict = {"data": {"username": "Marry", "password": 10}}

# Keyword arguments of request are created from merge of the two.
# record_dict has priority over target if common keys exists.
request_kwargs = {
    "url": "https://example.com/", "method": "POST",  "data": {
        "username": "Marry", "password": 10}
}
```
> `record_dict` will have to be created manually from _table record_.

Its best to have target hold only information that wont change and let record
hold information that may change like 'username' and 'password'.   

Session can also be provided as _dict_ with arguments pass when creating session.


> Basics of [broote](https://github.com/sekgobela-kevin/broote) are 
required to continue.


Webrute already provides connector which is used for making request at 
target but being able to define connector can be fun.
```python
import webrute

def connector(target, record, session=None):
    # Creates new record containing 'data' field.
    # Record gets tranformed before being passed to connector.
    new_record = webrute.record()
    new_record.add_item("data", dict(record))
    # webrute.connector() performs request and return response.
    return webrute.connector(target, new_record, session)
```
> Session is set by default which is shared by all requests.  

Connector is now combined with `success()`, `failute()` and `target()` 
functions.
```python
import webrute

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
    return response.is_success
```

> Target reached by default is True when status code is between 2XX.

Creating request can take some time if not executed in parallel or 
concurrently. Using `webrute.thread_runner` runner is best choice as it uses
threads for performing bruteforce.
```python
# Code for table is at top.
# ... ... ... ... ... ... .

# Code for success(), failure() and connector() at top.
# ... ... ... ... ... ... ... ... ... ... ... ... ... .

# Creates target dict containing url and method of request.
target = {"url": "https://example.com/login", "method": "POST"}

# target_reached and connect arguments are optional.
# Atleast one between success and failure needs to be provided.
runner = webrute.create_thread_runner(
    target, 
    table, 
    connector=connector, 
    success=success, 
    failure=failure
)

# Starts requests using connector()
runner.start()
runner.get_success_records() # [{'username': 'Marry', 'password': 8}]
```

`webrute.create_async_runner` creates runner using asyncio which may be 
faster than threads.
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
    return b"logged in as " in response.read()

async def failure(response):
    return b"Username and password does not match" in response.read()


# Creates target dict containing url and method of request.
target = {"url": "https://example.com/login", "method": "POST"}

# Creates runner executing using asyncio
runner = webrute.create_async_runner(
    target, 
    table, 
    connector=connector,
    success=success, 
    failure=failure
)
```
> [https://example.com/login](https://example.com/login) is not guaranteed
to exist or return responses as used above.

Connector in most cases can be avoided by using separate function for
transforming record. `record_transformer` argument can be passed which
is function for transforming record.

```python
def transformer(record):
    # Returns new record containing 'data' key.
    new_record = webrute.record()
    new_record.add_item("data", dict(record))
    return new_record

# Realise that 'connect' argument is not provided.
runner = webrute.create_thread_runner(
    target, 
    table,
    success=success, 
    failure=failure,
    record_transformer=transformer
)
```

> More features are available through 'broote' library.


### License
Webrute is released as open-source under conditions of 
[GPL-3.0](https://github.com/sekgobela-kevin/webrute/blob/main/LICENSE)
license.