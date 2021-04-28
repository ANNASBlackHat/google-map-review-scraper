###How to run the code?

1. Run Selenium
```
docker run -d -p 4444:4444 -p 7900:7900 -v /dev/shm:/dev/shm selenium/standalone-firefox:4.0.0-beta-3-20210426
```
find the latest version: https://github.com/SeleniumHQ/docker-selenium      

2. Create Virtual Environment and install required libraries
```
virtualenv venv
source venv/bin/activate
```

3. Run the code
```
python app.py
```     
