# Lions - Part Task Trainer
A web server created to validate student learning in part task trainers and to guide through cyber skills training exercises.

## Setup
- Create keys.py with ```secret_key = 'SOME_TEXT'```

## Downloads
- Download bootstrap.js from https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js
- Download jquery.js from https://code.jquery.com/jquery-3.2.1.slim.min.js
- Download bootstrap.css from https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css
- Download popper.js from https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js

### Docker Setup
[Click here for instructions](Dockerize.md)

## Goals
- Create a web UI that students can input answers into part task trainer exercises
- Future: Use the web server to query current state in remote machines in order to validate answers (think a question/problem that requires student to remove malicious activity from a device and the server can check whether the student was successful or not)

## Potential Uses
- WIC Trials
  - Note: Would require a public facing server
- PTT/WST/OST/DST
- Replacement for WS Look Scantron

## Features
- Rich user management
- View academics, lab guides and assessments all in the same UI
- Detailed metrics for each PTT to highlight student learning
- *Future:* Feedback built in to academics, giving students the ability to highlight specific parts that are confusing or need more information

## Problems Solved
- Formatting
  - Currently no standard set, this sets the standard for a professional looking training presentation
- Authoritative source of documentation
  - Currently difficult to find an authoritative source for where training is stored, adding the ability to dictate server XYZ or a specific revision could benefit change management
- Version control
  - Using a standardized ingestion format (.pdf's) and the exercise questions (.json) which is loaded on server start, this requires a server restart to update the academics and incrementing the version of said academics
- Ease of access
  - All the academics, lab guides and assessments are all stored in the same place allowing ease of access on the student as well as a well compiled library for access by instructors