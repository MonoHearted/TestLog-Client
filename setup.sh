#! /bin/bash

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

cd $SCRIPTPATH;
rpm -iU rpm/libffi-devel-3.0.13-18.el7.x86_64.rpm;
rpm -iU rpm/zlib-1.2.7-18.el7.x86_64.rpm;
rpm -iU rpm/zlib-devel-1.2.7-18.el7.x86_64.rpm;

tar vxf Python-3.7.3.tar.xz
cd Python-3.7.3
./configure --enable-optimizations
make
make altinstall
cd ..
ln -s /usr/local/bin/pip3.7 /usr/local/bin/pip3
ln -s /usr/local/bin/python3.7 /usr/local/bin/python3

rm -rf Python-3.7.3

pip3 install -r requirements.txt --no-index --find-links wheelhouse

echo \nPython 3 installation and package setup complete.
echo -e Don\'t forget to set self_address in config/logman.ini.
