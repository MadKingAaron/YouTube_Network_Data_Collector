
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from os.path import exists
# from webdriver_manager.chrome import ChromeDriverManager
import time, datetime
import subprocess, shlex
import re, os

CAP_FOLDER = './Captures'

def ensure_folder(folder_name):

    # Check if folder exists
    exists = os.path.exists(folder_name)

    if not exists:
        # Create folder 
        os.makedirs(folder_name)

def check_if_has_hours(time):
    pattern = re.compile(r"[0-9]+:[0-9]+:[0-9]+", re.IGNORECASE)
    return pattern.match(time)

def check_if_no_hours(time):
    pattern = re.compile(r"[0-9]+:[0-9]+", re.IGNORECASE)
    return pattern.match(time)

class YouTube_Viewer():
    def __init__(self, video_url, resolution='480p', browserDriverPath='./chromedriver', loadWaitTime=2, headless=True) -> None:
        self.video_url = video_url
        self.resolution = resolution
        self.browserDriverPath = browserDriverPath
        self.loadWaitTime = loadWaitTime
        self.scraper = self.__setup_youtube_scraper(headless=headless)
        self.videoLength = self.__get_video_length()
        self.video_title = self.__get_video_title()
        
        ensure_folder(folder_name=CAP_FOLDER)
    
    def __setup_youtube_scraper(self, headless=True):
        options = Options()
        if headless:
            options.add_argument('--headless')
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--mute-audio")
        #Load Chrome and get URL
        service = Service(self.browserDriverPath)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(self.video_url)
        #Wait for page to load
        print('Waiting %d sec(s) to load' %self.loadWaitTime)
        for i in range(self.loadWaitTime):
            print(i)
            time.sleep(1)

        title = driver.find_element(By.CSS_SELECTOR, "h1.title.style-scope.ytd-video-primary-info-renderer > yt-formatted-string.style-scope.ytd-video-primary-info-renderer").get_attribute("innerHTML")
        print(title)
        return driver
    
    def __get_folder_dir(self, video_title):
        return CAP_FOLDER+'/'+video_title+'.pcap'

    def __set_folder_dir(self):
        return self.__get_folder_dir(self.video_title)

    def __check_files_for_dup(self, video_title):
        return exists(self.__get_folder_dir(video_title))

    def __set_video_pcap(self, video_title):
        number = 1
        new_title = video_title
        while self.__check_files_for_dup(new_title):
            new_title = video_title + '_' + str(number)
            number += 1
        return new_title

    def __get_video_title(self):
        video_title = self.scraper.find_element(By.CSS_SELECTOR, "h1.title.style-scope.ytd-video-primary-info-renderer > yt-formatted-string.style-scope.ytd-video-primary-info-renderer").get_attribute("innerHTML")
        return self.__set_video_pcap(video_title)
    
    def __get_video_length(self):
        # Obtain the length of the youtube video
        duration = self.scraper.find_elements_by_xpath("//span[@class='ytp-time-duration']")[0].text
        print(duration)

        
        # Obtain the length of the video in seconds
        if (check_if_has_hours(duration)):
            x = time.strptime(duration, '%H:%M:%S')
            x1 = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
        elif (check_if_no_hours(duration)):
            x = time.strptime(duration, '%M:%S')
            x1 = datetime.timedelta(minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
        else:
            return

        return x1 #+ 1 #Add 1 second to prevent stopping early

    def __set_resolution(self):
        # Don't bother selecting resolution for Auto
        if self.resolution == 'Auto':
            print("Playing in Auto resolution.")
            return True
        self.scraper.find_element_by_css_selector('button.ytp-button.ytp-settings-button').click()
        self.scraper.find_element_by_xpath("//div[contains(text(),'Quality')]").click()

        time.sleep(2)   # you can adjust this time
        quality = self.scraper.find_element_by_xpath("//span[contains(string(),'%s')]" %self.resolution)
        print("Element is visible? " + str(quality.is_displayed()))

        quality.click()
        """ print("Selecting resolution...")
        time.sleep(0.2)
        sb = self.scraper.find_element_by_css_selector('.ytp-button.ytp-settings-button')
        sb.click()
        time.sleep(0.3)
        try:
            elem = self.scraper.find_element_by_css_selector('div.ytp-menuitem:nth-child(5) > div:nth-child(1)')
            elem.click()
        except:
            elem = self.scraper.find_element_by_css_selector('div.ytp-menuitem:nth-child(4) > div:nth-child(1)')
            elem.click()
        time.sleep(1)
        res = self.scraper.find_elements_by_class_name("ytp-menuitem-label")
        for item in res:
            #print(item.text)
            if self.resolution in item.text:
                item.click()
                print("Selected", self.resolution)
                return True
        return False """
    
    def __start_tcpdump(self)->subprocess.Popen:
        print("Saving capture to:",self.__set_folder_dir())
        proc = subprocess.Popen(['tshark','-w', self.__set_folder_dir()], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE,universal_newlines=True)
        proc.stdin.flush()
        return proc
    
    def __end_tcpdump(self, tcpdump:subprocess.Popen):
        kill = subprocess.Popen(shlex.split('kill '+str(tcpdump.pid)), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

    def start_video(self):
        try:
            self.__set_resolution()
        except:
            pass
        # Get the movie player
        video = self.scraper.find_element_by_id('movie_player')
        
        # Start tcpdump
        tcpdump =self.__start_tcpdump()
        #print(tcpdump.stdout.read())
        print('Play!')
        time.sleep(2)
        
        #Hit play on video
        video.send_keys(Keys.SPACE) #hits space
        time.sleep(self.videoLength)
        
        #Stop video
        video.click()
        print('Video stopped')
        
        # End tcpdump
        self.__end_tcpdump(tcpdump)
        
        time.sleep(5)
        print('Done!')
    
    def stop_session(self):
        self.scraper.close()

