# sdc-1-quickstart-python
The SPIN remote SDC-1 QuickStart app for Python

This a sample script showing how to connect the [SPIN remote SDC-1](http://spinremote.com), in Python.
This includes setting the LED color and receiving notifications. All is done in pretty much the same way as the [Android Quickstart](https://github.com/SPINremote/sdc-1-quickstart-android) app does.

The script uses the [PyYAML](http://pyyaml.org) lib and [bluepy](https://github.com/IanHarvey/bluepy) (only for Linux).
It has been tested in Python 2.7 and 3.4 on both a Raspberry Pi 3 using the built-in bluetooth and a Raspberry Pi 2 using bluetooth in the USB.

## Installation on a Raspberry Pi on Raspbian
1. Install Git, Python3 (though 2 works as well) and libglib: `sudo apt-get install git python3 python3-pip libglib2.0-dev`
2. Clone this repository: `git clone https://github.com/BillyNate/sdc-1-quickstart-python.git`
3. Go into the newly created directory: `cd sdc-1-quickstart-python`
4. Use pip to install requirements: `sudo pip3 install -r requirements.txt`
5. Start the script: `sudo python3 ./sdc-1-quickstart.py` (needs root to access the bluetooth)

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :)

## License
[MIT License](LICENSE)