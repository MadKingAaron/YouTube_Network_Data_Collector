from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
import time, datetime
import subprocess, shlex




class YouTube_Viewer():
    def __init__(self, video_url, resolution='480p', browserDriverPath='./chromedriver', loadWaitTime=2, headless=True) -> None:
        self.video_url = video_url
        self.resolution = resolution
        self.browserDriverPath = browserDriverPath
        self.loadWaitTime = loadWaitTime
        self.scraper = self.__setup_youtube_scraper(headless=headless)
        self.videoLength = self.__get_video_length()
        self.video_title = self.__get_video_title()
    
    def __setup_youtube_scraper(self, headless=True):
        options = Options()
        if headless:
            options.add_argument('--headless')
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
    
    def __get_video_title(self):
        return self.scraper.find_element(By.CSS_SELECTOR, "h1.title.style-scope.ytd-video-primary-info-renderer > yt-formatted-string.style-scope.ytd-video-primary-info-renderer").get_attribute("innerHTML")
    
    def __get_video_length(self):
        # Obtain the length of the youtube video
        duration = self.scraper.find_elements_by_xpath("//span[@class='ytp-time-duration']")[0].text

        # Obtain the length of the video in seconds
        x = time.strptime(duration, '%M:%S')
        x1 = datetime.timedelta(minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
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
    
    def __start_tcpdump(self,password:str)->subprocess.Popen:
        proc = subprocess.Popen(['sudo', '-S','tcpdump', '-n','-s', '0','-w', self.video_title+'.pcap', '-p'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE,universal_newlines=True)
        
        try:
            proc.stdin.write((password + '\n'))
        except:
            proc.stdin.write((password + '\n').encode())
        proc.stdin.flush()
        return proc
    
    def __end_tcpdump(self, tcpdump:subprocess.Popen, password:str):
        # print(tcpdump.stdout.read())
        kill = subprocess.Popen(shlex.split('kill '+str(tcpdump.pid)), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            kill.stdin.write((password + '\n').encode())
        except:
            kill.stdin.write((password + '\n'))
        kill.stdin.flush()

    def start_video(self, password:str):
        password = password.strip()
        try:
            self.__set_resolution()
        except:
            pass
        # Get the movie player
        video = self.scraper.find_element_by_id('movie_player')
        
        # Start tcpdump
        tcpdump =self.__start_tcpdump(password)
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
        self.__end_tcpdump(tcpdump, password)
        
        time.sleep(5)
        print('Done!')
    
    def stop_session(self):
        self.scraper.close()

        
""" def get_video_time(driver):
    # Obtain the length of the youtube video
    duration = driver.find_elements_by_xpath("//span[@class='ytp-time-duration']")[0].text

    # Obtain the length of the video in seconds
    x = time.strptime(duration, '%M:%S')
    x1 = datetime.timedelta(minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
    return x1 #+ 1 #Add 1 second to prevent stopping early

def start_video(driver, timeToWatch):
    #Get the movie player
    video = driver.find_element_by_id('movie_player')
    print('Play!')
    time.sleep(2)
    
    #Hit play on video
    video.send_keys(Keys.SPACE) #hits space
    time.sleep(timeToWatch)
    
    #Stop video
    video.click()
    print('Click')
    time.sleep(1)
    print('Done!')

def load_page(chromeDriverPath:str, url:str, loadWaitTime:int):
    #Load Chrome and get URL
    service = Service(chromeDriverPath)
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    #Wait for page to load
    for i in range(loadWaitTime):
        print(i)
        time.sleep(1)
    return driver

def watch_video(chromeDriverPath:str, url:str, loadWaitTime:int):
    driver = load_page(chromeDriverPath, url, loadWaitTime)
    total_runtime = get_video_time(driver)
    start_video(driver, total_runtime)


# watch_video('./chromedriver', 'https://www.youtube.com/watch?v=w6YeJOYOOds', 2)
# youtube_video = YouTube_Viewer('https://www.youtube.com/watch?v=w6YeJOYOOds')
# youtube_video.start_video()

service = Service('./chromedriver')
driver = webdriver.Chrome(service=service)
driver.get('https://www.youtube.com/watch?v=DXUAyRRkI6k')
# wait for the page to load everything (works without it)
for i in range(10):
    print(i)
    time.sleep(1)

video = driver.find_element_by_id('movie_player')
print('Play!')
time.sleep(2)
video.send_keys(Keys.SPACE) #hits space
time.sleep(1)
video.click()
print('Click')
time.sleep(1)
print('Done!') """