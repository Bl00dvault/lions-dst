# Lions - Part Task Trainer
A testing web server created to validate student responses to test questions and to guide through defensive skills training exercises.

## Goals
- Create a web UI that students can input answers into part task trainer exercises
- Future: Use the web server to query current state in remote machines in order to validate answers (think a question/problem that requires student to remove malicious activity from a device and the server can check whether the student was successful or not)

## TODO
[ ] Fix session so it does not persist filled in answers after server restarts
[x] Add login functionality
[ ] Add functionality to store student answers by username and attempt
[ ] Add test to see if 'tmp' folder exists to hold db, and if it doesn't exist to create it
[ ] Add admin login to clear all answers or clear answers for specific exercise and for specific student
[ ] Add option on results to show the correct answer if you press a button next to the question
[ ] Build user stories to help optimize
[ ] Build automated test cases
[ ] Pretty up UI, and add 32 WPS logo to title
