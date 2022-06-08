# YouTube Network Data Collector

    python3 runner.py <password>
## Dependencies

 - Selenium
 - Chrome Web Driver (in root of project folder)
 - Google Chrome installation


## Docker

 - run "sudo dockerd" to start docker daemon
 - start a new terminal, go to the ...Data_Collector directory, and run "sudo docker build . -t [name]" to build the docker container. You can put any names you want for [name] and [container name] just make sure they're different. Note that [name] and [container name] are different, [name] is for the docker image but [container name] is for the container.
 - run "sudo docker run -it --cap-add=NET_RAW --cap-add=NET_ADMIN --name [container_name] [name]" to run the runner.py script in the docker container
 - to get container contents out of container and copied to a tmp folder run "sudo docker cp [container name]:/app ./tmp" -- pcap files will be inside ./tmp
 - run "sudo docker rm -f $(sudo docker ps -a -q)" to remove all old containers
 - if removing containers isn't freeing up disk space run "sudo docker image prune -f"


Commands to copy:
 - sudo dockerd
 - sudo docker build . -t img
 - sudo docker run -it --cap-add=NET_RAW --cap-add=NET_ADMIN --name container img
 - sudo docker cp container:/app ./tmp
 - sudo docker rm -f $(sudo docker ps -a -q)
 - sudo docker image prune -f

## Packet Conversion

 - Make sure to all captures are in the `./Capture` folder created when capturing packets. 
 - Run `pcap_to_csv.py` for Linux/Mac OS or `pcap_to_csv_win.py` for Windows systems

 

 
