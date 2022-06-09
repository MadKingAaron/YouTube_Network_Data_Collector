
# YouTube Network Data Collector

Data Collection and Data Manipulation/Packet Conversion blocks of the OpenTracer pipeline

 - Data collection code in runner.py and video_viewer.py
 - Packet conversion code in pcap_to_csv.py

The Feature Engineering and Learning blocks of OpenTracer can be found here:
[https://github.com/rhystracy/Chunk_Size_Predictor](https://github.com/rhystracy/Chunk_Size_Predictor)

## Data Collection

    python3 runner.py <password>
   As tshark captures must be run as sudo, pass password as an argument when running `runner.py`
   Captures are done as repeat captures of all videos as default, can change to one capture per video by changing the repeat variable to False in runner.py
## Packet Conversion

 - Make sure to all captures are in the `./Capture` folder created when capturing packets. 
 - Run `pcap_to_csv.py` for Linux/Mac OS or `pcap_to_csv_win.py` for Windows systems


## Dependencies
 - Selenium
 - Chrome Web Driver (in root of project folder)
 - Google Chrome installation


## To Use With Docker:
Move to the "docker" branch
 
