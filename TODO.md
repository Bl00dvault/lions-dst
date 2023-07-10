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
  - [ ] Add error checking to do show message if already an admin
- [x] 7/7 Add admin only page to show current users
- [x] 7/8 Add storing user test scores per assignment (with additional data such as time to complete, right/wrong answers, etc.)

## UI
- [x] 7/7 Pretty up UI, and add 32 WPS logo to title
- [x] 7/8 Add sidebar or some other mechanism of storing admin actions
  - 7/8 Added significant changes to base.html and revamped the sidebar, incorporating Google Classroom and Canvas elements
- [x] 7/8 Research adding Google classroom/Canvas UI elements
  - [x] 7/8 [Google Classroom](https://www.youtube.com/watch?v=uODTp4yHXpI)
  - [x] 7/8 [Canvas](https://www.youtube.com/watch?v=PVfkFD45hL0)
  - [ ] [Adobe Captivate](https://www.adobe.com/products/captivate.html)

## Exercises
- [x] 7/7 Add option on results to show the correct answer if you press a button next to the question 
- [x] 7/7 Add clear all answers option to top of exercise page
- [ ] Add format to ingest new exercise/PTT as files and have the web page display
  - [ ] Separate issue of academics, lab walkthrough, and assessment
- [ ] Add ability to display .pptx in web to have lessons alongside the exercise
- [x] 7/8 Add functionality to store student answers by username and attempt
  - [x] 7/9 Create a separate page that shows all test results that is organized by user
    - Required to create a separate table for TestResults which now stores the information by user
- [ ] Consider adding "close" answers if within X number of characters and provide feedback to student
- [ ] Add option to provide feedback or highlight specific portions of academics/lab guide/assessment that are confusing
- [ ] Add a way to increment the version of each exercise (whether updated from .json or from new .pdf)

## Debug
- [x] 7/9 Add test to see if 'tmp' folder exists to hold db, and if it doesn't exist to create it
- [ ] Fix all resources being loaded after every refresh (e.g., all static files)
- [ ] Build user stories to help optimize
- [ ] Build automated test cases
  - [ ] Unit tests for logins
  - [ ] Unit tests for exercises
- [ ] Separate out app.py into logical pieces using imports
  - [ ] Utilize blueprints
- [ ] Add help (?) page to talk through how to use the site (essentially the SOP) one for admins and one for students

