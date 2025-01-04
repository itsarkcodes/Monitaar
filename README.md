﻿# Montiaar
Web Application monitoring with flask.


## Setting up locally 
* Create a copy of `.env.sample` file and add all the details in the file.
* Install all dependencies with `requirements.txt` file.
* Run the server with `python3 app.py`


### Abstract
The web appliction uses a seprate thread to run a function that checks web application status every 5 minutes, If any website is down it sends messages to the slack bots mentioned in the configuration.

## 1. Home Page  
![image](https://github.com/user-attachments/assets/1bc4da39-47f3-4d2a-82bf-327b657436f6)  

## 2. Add Website Page  
![image](https://github.com/user-attachments/assets/43b1d601-7a15-4a73-925f-882454ec3f96)  

## 3. Alert on Slack  
![image](https://github.com/user-attachments/assets/73f1096c-d0ab-442a-9f1f-7db245d9215f)  

