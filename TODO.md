# TODO
## User Management
- [x] 7/7 Add login functionality
- [x] 7/7 Add admin login and default admin user
- [x] 7/7 Add functionality to change password (and for admin to change password of other users)
  - [x] 7/7 Add user_management page
  - [x] 7/7 Add functionality to delete users
  - [x] 7/7 Add error checking so you can't delete your own user
  - [x] 7/7 Add ability to see admins on the page
  - [x] 7/7 Add function to make a user admin
  - [ ] Add error checking to show message if user is already an admin
- [x] 7/7 Add admin only page to show current users
- [x] 7/8 Add storing user test scores per assignment (with additional data such as time to complete, right/wrong answers, etc.)
- [x] 7/10 Add option to be able to export test scores to a file
  - [ ] Formatting is kinda sloppy, need to fix
- [ ] Add ability to add multiple users at once with the same password (new class function)

## UI
- [x] 7/7 Pretty up UI, and add 32 WPS logo to title
- [x] 7/8 Add sidebar or some other mechanism of storing admin actions
  - 7/8 Added significant changes to base.html and revamped the sidebar, incorporating Google Classroom and Canvas elements
- [x] 7/8 Research adding Google classroom/Canvas UI elements
  - [x] 7/8 [Google Classroom](https://www.youtube.com/watch?v=uODTp4yHXpI)
  - [x] 7/8 [Canvas](https://www.youtube.com/watch?v=PVfkFD45hL0)
  - [ ] [Adobe Captivate](https://www.adobe.com/products/captivate.html)
- [ ] Change menu to be a dropdown sidebar, rather than just a button to allow for growth and submenus

## Exercises
- [x] 7/7 Add option on results to show the correct answer if you press a button next to the question 
- [x] 7/7 Add clear all answers option to top of exercise page
- [x] 7/9 Add format to ingest new exercise/PTT as files and have the web page display
  - Separate issue of academics, lab walkthrough, and assessment
- [x] 7/9 Add ability to display .pptx in web to have lessons alongside the exercise
  - Used the workaround of exporting .pptx to .pdf since it's only 3 clicks
- [x] 7/8 Add functionality to store student answers by username and attempt
  - [x] 7/9 Create a separate page that shows all test results that is organized by user
    - Required to create a separate table for TestResults which now stores the information by user
- [ ] Consider adding "close" answers if within X number of characters and provide feedback to student
- [ ] Add option to provide feedback or highlight specific portions of academics/lab guide/assessment that are confusing
- [ ] Add a way to increment the version of each exercise (whether it was updated from .json or from new .pdf)


## Packaging
- [x] 7/10 Create a dockerfile for easy transport of the webserver
  - [x] 7/16 Need to create a volume to store academics
  - [x] 7/16 Create procedure for uploading new academics to docker volume
- [x] 7/10 Test locally
- [ ] Test at work

## Debug
- [x] 7/9 Add test to see if 'tmp' folder exists to hold db, and if it doesn't exist to create it
- [x] 7/10 Create an automated method of updating the '__version__' variable in app.py based on code changes
  - Note: the version information corresponds to the following:
    - MAJOR version when you make incompatible API changes.
    - MINOR version when you add functionality in a backwards-compatible manner.
    - PATCH version when you make backwards-compatible bug fixes.
  - '__version__' can be updated manually using git hooks and a bash script, but for portability sake I'll just update it manually. Now displayed on / page.
- [ ] Fix all resources being loaded after every refresh (e.g., all static files)
- [ ] Build user stories to ensure all features are captured
- [ ] Build automated unit tests
  - [ ] Logins
  - [ ] Assessments
  - [ ] Displaying academics
  - [ ] Displaying lab guides
  - [ ] User management
- [x] 7/16 Separate out app.py into logical pieces using imports
  - [x] 7/16 Utilize blueprints
- [x] 7/16 Add help (?) page to talk through how to use the site (essentially the SOP) one for admins and one for students
- [ ] Add way for application to re-read exercises.json without having to restart the application/container
- [ ] Fix URL duplicating under exercises e.g., 'http://localhost:5001/exercise/exercise/4'
- [ ] Academics won't render on exercise_landing_page unless the Lab exists as well, add error checking to allow one to exist without the other
- [ ] Remove ability to take assessments when not logged in

## Cyber Trials
- [ ] Develop User Stories/System Design layout for Cyber Trials
- [ ] Deploy to an AWS instance
- [ ] Create 'trial' ranges that can be used to assess defensive cyber skills and critical thinking
  - [ ] Deploy ranges onto AWS using Ansible
  - [ ] Identify pricing for a typical cyber trial range
- [ ] Create scheduling module for Cyber Trials
  - [ ] Develop role schema to allow trials admins to schedule range time
- [ ] Update the help page for Cyber Trials
