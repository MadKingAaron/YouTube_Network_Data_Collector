FROM python:3.8

COPY . /app
WORKDIR /app

### Install tcpdump
RUN apt-get update && apt-get install -y tcpdump

### Install chrome in docker image:

# Adding keys to apt for repositories

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Get chrome

RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -y update

RUN apt-get install -y google-chrome-stable


### Install Chrome Driver:

# Installing unzip

RUN apt-get install -yqq unzip

# Get chrome driver

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin


# Set display port as an environment variable

ENV DISPLAY=:99


### Run Script

RUN pip install --upgrade pip

RUN pip install selenium
#==4.0.0a5

CMD ["python", "runner.py"]