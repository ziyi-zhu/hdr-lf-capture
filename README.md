# HDR Light Field Capture
Hardware and software for capturing Hight Dynamic Range light fields

![](image/header.jpg)

## Arduino

### Wiring

![](image/arduino.jpg)

The Stepper Driver used in this setup is DQ542MA and the Stepper Motor used is NEMA 17 42BYGH-W811.

Connection Driver to Arduino:
* PUL+ from Driver to Arduino PIN7
* PUL- from Driver to Arduino PIN5
* DIR+ from Driver to Arduino PIN7
* DIR- from Driver to Arduino PIN6
* ENBL+ from Driver to Arduino PIN7

Connection Driver to Stepper:
* A+ from Driver to Stepper BLACK wire
* A- from Driver to Stepper GREEN wire
* B+ from Driver to Stepper RED wire
* B- from Driver to Stepper BLUE wire

Connection Button to Arduino:
* Button YELLOW wire to Arduino PINA0

### Power Supply

![](image/battery.jpg)

The power supply for the Stepper Driver is 18V (3 parallel sets of 2 9V batteries in series).

## Python
### Dependencies

Installing libgphoto2:

```sh
sudo apt-get install libgphoto2-dev
```

Installing python-gphoto2 for python3 with pip:

```sh
sudo pip3 install gphoto2
```

Installing pySerial for python3 with pip:

```sh
sudo pip3 install pyserial
```

## Release History

* 0.1.0
    * The first proper release
    * CHANGE: Add `arduino` and `python`
* 0.0.1
    * Work in progress