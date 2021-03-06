# poly2gcal

Add PolyMTL classes to Google Calendar.

* supports both lectures and labs
   * lecture event title format: "Cours - ${class_name}"
   * lab event title format: "Lab - ${class_name}"
* supports B1/B2 week alternation and exceptions
* supports break week and holidays
* creates one calendar per class

https://xkcd.com/1319/

## Prerequisites

This has only been tested with **Python 3**.

To install dependencies:

```shell
$ pip3 install -r requirements.txt
```

## Usage

1. add course data to [`input_data.json`](./input_data.json) (or modify the existing one)

2. get Google Calendar API access through [Google API Console](https://console.developers.google.com/) and place your `client_secrets.json` file in this directory (you may have to rename it); see [here](https://github.com/googleapis/google-api-python-client/blob/master/docs/client-secrets.md)
   * on first use, it will ask you to login and allow it to modify your calendar

3. run
   ```shell
   $ ./poly2gcal.py
   ```
   if you only want to see the resulting events without actually adding them to your calendar (e.g. to validate), use
   ```shell
   $ ./poly2gcal.py --test
   ```
   for more options
   ```shell
   $ ./poly2gcal.py --help

4. check your Google calendar
   * each class has its own calendar
   * make sure to validate the result

## Input format

In general:

* date format is `YYYY-MM-DD`
* time format is `0123` (e.g. `0830` for 8:30 AM)
* exam period is not considered as being part of the semester when it comes to classes/lectures/labs
* by default, the week with the first day of the semester is B1, and the next week is B2, etc., and the break week is skipped

Format description for `input_data.json`:

* `semester_info`
   * `first_day`: date of first actual day of the semester
   * `last_day`: date of last actual day of the semester (excluding the exam period)
   * `breakweek_day`: date for Monday of the mid-semester break week
   * `holidays`: dates for holidays during the semester (no classes or labs or anything), or empty/not set
   * `alt_exceptions`: dates on which to start flipping the week alternation (e.g. B1 to B2) TODO (or empty/not set)
      * example: "2020-09-14" (Monday September 14 2020) --> all Mondays from 2020-09-14 onwards will be flipped
* `courses`
   * content for one course:
      * `name`: name of the course (used as the name for the class' calendar and in the calendar events)
      * `id`: course ID (e.g. ABC1234) or empty/not set; not used
      * `lectures`
         * content for one lecture
            * `day`: day of the week (e.g. Monday)
            * `start`: start time
            * `duration`: duration in number of 50-minute blocks (e.g. a lecture from 0830 to 1120 has a duration of 3)
            * `room`: location/room (or empty/not set)
            * `description`: description to use for all these events (or empty/not set)
      * `labs`
         * content for one lab
            * `day`: see above
            * `start`: see above
            * `duration`: see above
            * `room`: see above
            * `description`: see above
            * `week`: B1 or B2 if alternating between weeks/biweekly, or empty/not set if weekly

## TODO

* get course info (lecture/lab times) from PolyMTL's website
