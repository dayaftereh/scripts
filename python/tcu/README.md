# TCU

TCU stands for *Temperature Control Unit* and is developed to run on [Odroid XU4](http://www.hardkernel.com/main/products/prdt_info.php?g_code=G143452239825).
TCU reads the cpu temperature, checks temperature thresholds and switch a *GPIO* at the *Odroid XU4* on, if the temperature is above the defined thresholds.

## Dependencies
 * Ubuntu 16.04
 * Linux Kernel 3.10.104-127+

## Usage

TCU has a simple ```setup.sh``` for installing or removing TCU from the Odroid XU4. 
Additionally TCU cam with [systemd](https://wiki.debian.org/systemd) service files to get executed more easier.

### Install & Removing
TCU can be installed with ```setup.sh``` and the parameter **install**. 
The ```setup.sh``` script install TCU to the path ```/opt/tcu```.
```bash
#> cd tcu/
#> sudo ./setup.sh install
update-alternatives: /opt/tcu/tcu.py is used for /usr/bin/tcu
good bye
```
TCU can be removed easily by executing ```setup.sh``` with **remove**:
```bash
#> sudo /opt/tcu/setup.sh remove
good bye
```

### via Systemd
After the installation, *systemd* can be used to started, checked and stopped TCU.
For starting TCU with *systemd* use the following command:
```
#> sudo systemctl start tcu.service
```

For checking the status of TCU with *systemd*, use the next command:
```
#> sudo systemctl status tcu.service
tcu.service - Temperature Control Unit
   Loaded: loaded (/opt/tcu/tcu.service; linked; vendor preset: enabled)
   Active: active (running) since Di 2017-01-01 00:00:00 UTC; 1min ago
 Main PID: 1001 (tcu)
   CGroup: /system.slice/tcu.service
           └─1001 /usr/bin/python /usr/bin/tcu --log INFO --config /opt/tcu/config.json --pidfile /var/run/tcu.pid

Jan 01 00:00:00 odroid systemd[1]: Started Temperature Control Unit.
Jan 01 00:00:00 odroid tcu[1001]: 01-01-2017 00:00:00 :: [  INFO ] :: using log level [ INFO ]
Jan 01 00:00:00 odroid tcu[1001]: 01-01-2017 00:00:00 :: [  INFO ] :: pid file written to [ /var/run/tcu.pid ] with pid [ 1001 ]
Jan 01 00:00:00 odroid tcu[1001]: 01-01-2017 00:00:00 :: [  INFO ] :: loaded configuration from [ /opt/tcu/config.json ]
Jan 01 00:00:00 odroid tcu[1001]: 01-01-2017 00:00:00 :: [  INFO ] :: fan controller as been started.
Jan 01 00:00:00 odroid tcu[1001]: 01-01-2017 00:00:00 :: [  INFO ] :: cpu-tmu-reader has been started.
Jan 01 00:00:00 odroid tcu[1001]: 01-01-2017 00:00:00 :: [  INFO ] :: tcu has been started in [ 0.0069 s ].
```

To stop the TCU with *systemd*, use the following command:
```
#> sudo systemctl stop tcu.service
```
