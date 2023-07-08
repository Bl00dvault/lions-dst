# Lions - Part Task Trainer
A testing web server created to validate student responses to test questions and to guide through cyber skills training exercises.

## Goals
- Create a web UI that students can input answers into part task trainer exercises
- Future: Use the web server to query current state in remote machines in order to validate answers (think a question/problem that requires student to remove malicious activity from a device and the server can check whether the student was successful or not)

## TODO
### User Management
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

### UI
- [x] 7/7 Pretty up UI, and add 32 WPS logo to title
- [ ] Add sidebar or some other mechanism of storing admin actions
- [ ] Research adding Google classroom/Canvas UI elements
  - [ ] [Google Classroom](https://www.youtube.com/watch?v=uODTp4yHXpI)
  - [ ] [Canvas](https://www.youtube.com/watch?v=PVfkFD45hL0)

### Exercises
- [x] 7/7 Add option on results to show the correct answer if you press a button next to the question 
- [x] 7/7 Add clear all answers option to top of exercise page  
- [ ] Add functionality to store student answers by username and attempt
- [ ] Consider adding "close" answers if within X number of characters and provide feedback to student

### Debug
- [ ] Add test to see if 'tmp' folder exists to hold db, and if it doesn't exist to create it
- [ ] Build user stories to help optimize
- [ ] Build automated test cases
  - [ ] Unit tests for logins
  - [ ] Unit tests for exercises
- [ ] Separate out app.py into logical pieces using imports
  - [ ] Utilize blueprints

