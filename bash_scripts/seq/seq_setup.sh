#!/bin/bash
trimmomatic=http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.39.zip
picard=https://github.com/broadinstitute/picard/archive/2.23.3.tar.gz

sudo apt-get -y update
sudo apt-get -y upgrade

mkdir ~/seq_tools
cd ~/seq_tools

wget $trimmomatic
unzip ${trimmomatic##*/}
rm ${trimmomatic##*/}

sudo apt-get -y install bwa

wget $picard
tar -zxf ${picard##*/}
rm ${picard##*/}

sudo apt-get -y install python3-pip
pip3 install astair


sudo reboot
