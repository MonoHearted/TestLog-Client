===================
NGLogman Clientside
===================

This program can be run in either standalone mode or in listening mode for use together with the NGLogman Serverside.

Before first execution, run setup.sh to install Python 3 and the required dependencies. If Python 3 is
already installed, you can comment out the third block in setup.sh starting with ``tar vxf Python-3.7.3.tar.xz``
up to ``ln -s /usr/local/bin/python3.7 /usr/local/bin/python3``.

Packaging for Distribution
---------------------------

1. Download "Python-3.7.3.tar.xz" and place in this directory.
2. Run ``python3 setup.py package``
3. The finished package can now be found under ``dist/``.

**IMPORTANT**: If run in server mode, edit config/logman.ini and change ``self_address`` to the current IP address of the machine.
Additionally, make sure the correct NGLogmanServer side gRPC address is set in the config.

Parameters
----------

::

    python3 NGLogmanClient.py [-s] [-ip $IP] [-c $CONFIGFILE] [-pn $PROCESSNAME] [-pid $PID] interval duration

- -s: Run in listening mode.
- -ip: Specify the remote server ip.
- -c: Specify a config file location. (Default: config/logman.ini)

Standalone Mode:
    - -pn / --process-name: Provide a process name for monitoring.
    - -pid / --process-id: Provide a process ID (PID) for monitoring.
    - interval: How often to generate data points.
    - duration: How long to run the task for.

Usage
------
General usage of this package is through server mode, in which this client will automatically
connect and register to the server IP set in the config. All operations here will be controlled
through the NGLogmanServer side, whether through the UI or the RESTful API. Excel outputs after
a task is completed can be found both locally and through the server.

In standalone mode, this will immediately start the Logman process with the command line parameters
provided. The excel document will be found under Output.


Credits
--------
- Ivor Chen (ivor.chen@genesys.ca)
- Bryan Niu (b3niu@edu.uwaterloo.ca)
