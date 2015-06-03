# User Story #

As a Volunteer Coordinator I want to add event-based tasks.

Work is tracked on [Issue 17](https://code.google.com/p/chirpradio/issues/detail?id=17)

See VolunteersCanClaimTasks for how Volunteers typically will want to claim tasks.

Up until now, tasks are ongoing.  For example "create flyers for Tony" would be a task that gets assigned to a Volunteer.  With the record fair, they need to **optionally** become event based.

The work flow should be like this using a single shift at the Record Fair as an example:

  * Create or select an event.  Enter name: Record Fair and dates: from April 18th - 19th.
  * Create a task that needs to be completed on 4/18
  * Create a shift that starts at 12pm and lasts 2 hours
  * Enter the number of volunteers needed for this shift (2)

# Technical notes #

  * The database will need updating.  Probably a new table for events is also needed.  It may be possible to add optional columns on the tasks table for this.  See the README in code about how database migrations work.
  * This probably needs a separate screen like the Meeting Tracker page defined in chirp/volunteers/views.py and chirp/volunteers/templates/meetings.html
  * If it makes sense to use JavaScript for hiding form values or whatever then jQuery and jQuery UI are available.  See meetings.html for an example of how to use those libraries.