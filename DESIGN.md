DESIGN DOCUMENT

As discussed in my documentation and video, Staffing Scheduler was inspired by necessity. I am, with the other co-directors, jointly responsible for generating staffing schedules for Contact Peer Counseling, which is staffed by two volunteer undergraduates each night of the week. We, like many organizations and businesses, try to evenly distribute the workload amongst our counselors, assigning shifts based on availability, preference, and number of shifts already staffed or assigned in a given cycle. Incorporating all of these variables into my hand-powered schedule generation for each cycle is a tiresome and time-consuming task, so I set out to automate this process with Staffing Scheduler while preserving our goal of honoring even workload distribution, availability, and preference. Furthermore, I expanded this program beyond the model of Contact's staffing structure to support variable numbers of total staffers and staffers per daily shift. In doing so, I accomplished both of my "good outcome" goals, as well as one of my two "better outcome" goals, which I consider a success.

The core functional engine of this program is the app.py code that facilitates the selection of the number of staffers total and per day, the storing of staffer availability data after each click of the "Submit" button, and then the tiered selection of the names of not-unavailable staffers for population and printing in the output Schedule table.

To achieve this, I first created a database containing a table called "dimensions" in which each new schedule's number of total staffers and staffers per day is stored, along with an auto-incrementing unique id number. I also created a table "staffers" to store the name of each staffer ("name"), the availability input of each day (name of day of week), an indicator of whether the staffer had already been assigned to a given day (the first two letters of the day name + 'Bool'), and a running count of the number of shifts they had already been assigned to ("shifts"). Finally, I created a table "output" that would store the names of assigned staffers in columns labeled for each day, as well as hold a row id for each row of assigned staffers.

When proceeding through the "New Schedule" form, a new row is added to "dimensions" that holds the user inputs after they click "Next." At this time, the "staffers" table is cleared to make room for the new set of incoming rows. The "total number of staffers" input is then accessed via the row id corresponding to the table length to limit the number of times that the staffer availability form can be submitted. Upon submission, each set of availabilities is stored in a new row in the "staffers" table.

Then, when the final staffer availability form is submitted, the "output" table is cleared to make room for the new schedule. First, an "empty" table of zeros is generated, with the number of rows corresponding to the inputted number of staffers per shift. Then, for each day in each row, the staffers who replied "Available" and are not already staffing on that day are selected and ordered by ascending number of shifts already assigned. From that selection, if any exist, the top staffer (the one currently staffing the fewest shifts overall) is selected and the output table is updated to reflect their name in that given row and day. That staffer is then marked as staffing that day (via updating the corresponding '__Bool' value) and their shift count is incremented by one. If there are no staffers for that day who are available and not already staffing that day, then the staffers who marked that day as "Prefer not to staff" and are not already staffing that day are selected and ordered by ascending number of shifts already assigned. Again, if any exist in that selection, the top name is picked and inserted into the output table in that row and day, that staffer's shift count is incremented, and that staffer is marked as staffing for that day. Finally, if no staffers meet either of these sets of criteria (meaning everyone is either unavailable or already staffing that day), the output table is updated to say "UNFILLED" at that day and row. Once this table is generated in the database, it is printed to the screen for the user to view. This table is cleared once the user navigates back to "Home" or "New Schedule" for quick and easy reuse.