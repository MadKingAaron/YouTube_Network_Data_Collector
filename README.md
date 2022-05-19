# YouTube Network Data Collector

    python3 runner.py <password>
## Dependencies

 - Selenium
 - Chrome Web Driver (in root of project folder)
 - Google Chrome installation


## Docker

 - run "sudo dockerd" to start docker daemon
 - start a new terminal, go to the ...Data_Collector directory, and run "sudo docker build . -t [name]" to build the docker container. You can put any name you want for [name]. Note that [name] and [container name] are different, you pick [name], docker picks [container name].
 - run "sudo docker run -it [name]" to run the runner.py script in the docker container
 - to get container contents out of container and copied to a tmp folder run "sudo docker cp [container name]:/app ./tmp" -- it's also possible that the pcap output is being stored in a weird place inside the container and not in /app where it should be, you can replace '/app' with just '/' to copy full contents of container (this is slow and takes a lot of storage space for some reason though and I couldn't find the pcap here at all)
 - to get [container name] run "sudo docker container ls -a" and use either the CONTAINER_ID value or NAMES value from the most recent container in place of [container name], both should work
 - run "sudo docker rm -f $(sudo docker ps -a -q)" to remove all old containers

 

 
