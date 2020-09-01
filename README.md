# poly2gcal

Add PolyMTL classes to Google Calendar

## Prerequisites

This has only been tested with **Python 3**.

To install dependencies:

```shell
$ pip3 install -r requirements.txt
```

## Usage

1. add course data to [`input_data.json`](./input_data.json)

2. get Google Calendar API access through [Google API Console](https://console.developers.google.com/) and place your `client_secrets.json` file in this directory (you may have to rename it); see [here](https://github.com/googleapis/google-api-python-client/blob/master/docs/client-secrets.md)

3. run
   ```shell
   $ ./poly2gcal.py
   ```
   if you only want to see the resulting events without actually adding them to your calendar, use
   ```shell
   $ ./poly2gcal.py -t
   ```

## TODO

* get course info (lecture/lab times) from PolyMTL's website
