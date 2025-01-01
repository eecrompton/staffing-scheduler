DOCUMENTATION

STRUCTURAL OUTLINE: Flask web application
    schedule folder:
        static folder:
            styles.css
        templates folder:
            index.html (main HTML template)
            apology.html
            new.html
            output.html
            staffers.httml
            welcome.html
        app.py
        requirements.txt
        schedule.db
        DESIGN.md
        README.md

SETUP
To compile and run this application, use the command "flask run" while within the schedule folder in cs50.dev. The generated link will open into a new window displaying the Staffing Scheduler home page.

APPLICATION OVERVIEW
Staffing Scheduler is a web application tool used to generate a weekly staffing schedule. This project was inspired by my need as co-director of Contact Peer Counseling to repeatedly generate weekly schedules for our staffers based on their availability and preferences. Generally, I do this by hand, assigning two staffers to each shift, with each staffer serving approximately the same number of shifts per schedule cycle. This application goes a step further, allowing for the generation of schedules for variable numbers of total staffers and staffers per shift.

NAVIGATING THE APPLICATION
Opening the web application after running Flask will bring a user to the home page, which instructs users to select the "New Schedule" button in the navigation bar above. The "Home" button redirects to the same home page and effectively has no extraneous function on this current page.

IMPORTANT TIP: Clicking the "Home" button will always redirect the user to a new home page and reset the Scheduler. This can be useful if the user wishes to start over.

Once the "New Schedule" button has been clicked, the user is directed to a page that requests the number of total staffers and the number of staffers to be assigned per daily shift. The user must input positive integers for this form, otherwise an error message will display. Return to the request page by re-clicking the "New Schedule" button or reloading the page.

Clicking "Next" will bring the user to the first staffer input page, as indicated by the "Staffer 1 of X" counter neear the top of the page. The user must input a name for the first staffer and select that staffer's availability for ach day of the week, according to the arrayed radio buttons. The form will not submit unless all of these fields are filled out.

Clicking "Submit" will bring the user to the next staffer availability input page until the "Staffer X of X" counter indicates the final staffer availability input page, in which instance the "Submit" button will generate the schedule and direct the user to the schedule output page. The schedule will prioritize assigining an equal number of shifts to each staffer, with the primary exception of if a staffer with fewer shifts has no more remaining available shifts. In this regard, "Prefer not to staff" designations are considered available, but they are prioritized secondary to the shifts each staffer designated as "Available." A staffer will never be assigned to a shift which they designated as "Unavailble." In the event that too few staffers are available (includng "prefer not to staff" designations) for a given shift compared to the number of staffers requested per daily shift, the Scheduler will mark the corresponding number of empty slots as "UNFILLED." Any "UNFILLED" slots will be oriented at the top of each column for optimal noticeability.

IMPORTANT TIP: The user can view this schedule until the "Home" or "New Schedule" buttons are selected, at which time the user will be redirected to the corresponding page, the generated schedule will be cleared, and a new scheduling implementation will commence.

Happy Scheduling!


Video URL: https://youtu.be/mcvU3RAryRo
