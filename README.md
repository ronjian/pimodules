This module is built on python3.  
Dependency:  
- [RPi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/wiki/install/)
- [pigpio](http://abyz.me.uk/rpi/pigpio/index.html)

Install steps:  
```shell
git clone https://github.com/ronjian/pimodules.git
cd	pimodules
python3 setup.py install
# verify 
python3 -c "import pimodules; print('pimodules installed successfully')"
```