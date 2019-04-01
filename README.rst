===================
NGLogman Clientside
===================

This program can be run in either standalone mode or in listening mode for use together with the NGLogman Serverside.

Packaging for Distribution
---------------------------

1. Download "Python-3.7.3.tar.xz" and place in this directory.
2. Run ``python3 setup.py package``
3. The finished package can now be found under ``dist/``.

Before first execution, run setup.sh to install Python 3 and the required dependencies.

**IMPORTANT**: If run in server mode, edit config/logman.ini and change ``self_address`` to the current IP address of the machine.

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

Credits
--------
- Ivor Chen (ivor.chen@genesys.ca)
- Bryan Niu (b3niu@edu.uwaterloo.ca)
