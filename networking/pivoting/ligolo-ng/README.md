# Pivoting with Ligolo  


[*Ligolo-ng*](https://github.com/nicocha30/ligolo-ng) is an advanced yet straightforward tunneling and pivoting tool designed for penetration testers to establish tunnels using a TUN interface over reverse TCP/TLS connections.  
Unlike traditional methods that rely on SOCKS proxies or TCP/UDP forwarders, Ligolo-ng employs a userland network stack via Gvisor, enabling seamless network traffic routing without the need for administrative privileges on the agent side.  
This design facilitates the execution of tools like Nmap without additional configurations, enhancing efficiency during security assessments.  
Key features of Ligolo-ng include automatic certificate configuration with Let's Encrypt, support for multiple platforms, and the capability to handle various protocols such as TCP, UDP, and ICMP.  
Its performance is notable, achieving speeds exceeding 100 Mbits/sec, making it a valuable asset for effective network pivoting in offensive security operations.  


## Getting started  

There are already many good resources and tutorials available that demonstrate how to use Ligolo-ng.  
Highly recommended by me are:  
1. [*The official Quickstart guide*](https://github.com/nicocha30/ligolo-ng/wiki/Quickstart)  
2. [*This Medium article*](https://software-sinner.medium.com/how-to-tunnel-and-pivot-networks-using-ligolo-ng-cf828e59e740)  
3. [*This video by John Hammond*](https://www.youtube.com/watch?v=qou7shRlX_s)  



