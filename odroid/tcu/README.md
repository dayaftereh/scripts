# TCU

TCU stands for Temperature Control Unit and is developed to run on [Odroid XU4](http://www.hardkernel.com/main/products/prdt_info.php?g_code=G143452239825). 
TCU reads the cpu and sensor temperature, checks temperature thresholds and turns on a GPIO at the *Odroid XU4*, if the temperature is above the defined thresholds.
The Temperature Control Unit is written in *C*, because internal the DHT22 sensor is used to measure the temperature.

## Dependencies

* Ubuntu 16.04
* Linux Kernel 3.10.104-127+
* wiringPi 2.38+

## Build Install

TCU can be install with **make**:
```
#> sudo make install
```
The command above builds and installs TCU on the system.
TCU is installed in */opt/tcu/*.
Additionally TCU gets controlled via [systemd](https://wiki.debian.org/systemd).

## via Systemd

After the installation, *systemd* can be used to start, check status and stop TCU from the command line. 

```
#> sudo systemctl start tcu.service
```
The command above starts TCU on the system.
For checking the status of TCU with systemd, use the next command:
```
#> sudo systemctl status tcu.service
tcu.service - Temperature Control Unit
   Loaded: loaded (/opt/tcu/tcu.service; linked; vendor preset: enabled)
   Active: active (running) since Di 2017-01-01 00:00:00 UTC; 1min ago
 Main PID: 1001 (tcu)
   CGroup: /system.slice/tcu.service
          └─1001 /opt/tcu/tcu --config /opt/tcu/config/tcu.conf --pidfile /var/run/tcu.pid

Jan 01 00:00:00 odroid systemd[1]: Started Temperature Control Unit.
```
To stop the TCU with systemd, use the following command:

```
#> sudo systemctl stop tcu.service
```