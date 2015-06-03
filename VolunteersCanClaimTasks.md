# User Story #

As Volunteer I want to login to the Volunteer Tracker and claim a task.

Work is tracked on [Issue 15](https://code.google.com/p/chirpradio/issues/detail?id=15)

The first iteration should be designed for signing up to do record fair tasks.  So more specifically:

As a volunteer I want to login to the Tracker and sign up for a shift
at the record fair.

In its simplest form the list of tasks to sign up for could look like this (however, there are details about this below) :

```
4/18 Tabling from 12pm - 2pm (3 volunteers needed)
4/18 Tabling from 2pm - 4pm (2 volunteers needed)
...etc...
```

# Some technical considerations #

  * After a task is claimed by the maximum number of volunteers it will no longer be available (grayed out?).
  * The backend should mark the TaskStatus as "Assigned"
  * The backend should **also** email the volunteer telling her something like: "You signed up for 4/18 Tabling from 12pm - 2pm"
  * a volunteer **must** sign up for a minimum number of shifts (two?).  Not sure yet how to accomplish this.
  * note that the record fair tasks are event-like and this has not been implemented yet.  A ticket is forthcoming to address this.
  * the site may be under concurrent load so transactions should be used for the claiming process.
  * The page for this can be a custom django page like the Meeting Tracker which is defined in chirp/volunteers/views.py and chirp/templates/admin/index.html
  * Before beginning work on this site, permissions need to be implemented to hide the custom Meeting Tracker page which is currently visible to anyone in chirp/templates/admin/index.html.

# User Experience #

The UI should show a calendar-like view where tasks are listed per event (record fair), per day, per shift in chronological order.  Note that this requires event-based changes to the DB per CoordinatorCanMakeEventTasks