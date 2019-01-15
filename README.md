# poly2gcal

Add PolyMTL classes to Google Calendar

## Prerequisites

This uses **Python 3**.

To install dependencies:
```
pip3 install --trusted-host pypi.python.org -r requirements.txt
```

## Usage

1. add course data to [`input_data.py`](./input_data.py)

2. get Google Calendar API access through [Google API Console](https://console.developers.google.com/)

3. run
   ```
   ./poly2gcal.py
   ```
   if you only want to see the resulting events without actually adding them to your calendar, use
   ```
   ./poly2gcal.py -t
   ```

## TODO

* support labs (non-weekly events)
* use JSON format for input data
