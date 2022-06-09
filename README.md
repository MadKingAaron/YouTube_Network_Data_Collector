
# YouTube Network Data Collector

Data Collection and Data Manipulation/Packet Conversion blocks of the OpenTracer pipeline

 - Data collection code in runner.py and video_viewer.py
 - Packet conversion code in pcap_to_csv.py

The Feature Engineering and Learning blocks of OpenTracer can be found here:
[https://github.com/rhystracy/Chunk_Size_Predictor](https://github.com/rhystracy/Chunk_Size_Predictor)

## Data Collection

    python3 runner.py <password>
   As tshark captures must be run as sudo, pass password as an argument when running `runner.py`
## Packet Conversion

 - Make sure to all captures are in the `./Capture` folder created when capturing packets. 
 - Run `pcap_to_csv.py` for Linux/Mac OS or `pcap_to_csv_win.py` for Windows systems


## Dependencies
 - Selenium
 - Chrome Web Driver (in root of project folder)
 - Google Chrome installation

 
