#  CONTAINER BREAKOUT CTF
You found a web portal, it is an application to read file inside a container, are you able to find the flag?  

## Prepare the Challenge

> WARNING  
> Put this in a isolated Virtual Machine!!

1. On the host VM, put your flag in `/root/flag.txt`:  
```sh
echo "CTF{your_flag_content}" > /root/flag.txt
```  

2. Launch the container on the VM:  
```sh
docker build -t containify . && docker run -d -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock containify
```  


If you are stuck, follow the [*walkthrough*](./walkthrough/README.md).  
  
