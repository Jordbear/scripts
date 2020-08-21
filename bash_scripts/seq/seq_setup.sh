#!/bin/bash
trimmomatic_link=http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.39.zip
picard_link=https://github.com/broadinstitute/picard/releases/download/2.23.3/picard.jar

sudo apt-get -y update
sudo apt-get -y upgrade

mkdir ~/seq_tools
cd ~/seq_tools

wget $trimmomatic_link
timmomatic_compressed=${trimmomatic_link##*/}
sudo apt-get install -y unzip
unzip $timmomatic_compressed
rm $timmomatic_compressed
trimmomatic_jar=`pwd`'/'${timmomatic_compressed%%.zip}'/'${timmomatic_compressed%%.zip}'.jar'
echo '$TRIMMOMATIC="'$trimmomatic_jar'"' >> ~/.bashrc

sudo apt-get -y install bwa

sudo apt-get -y install samtools

wget $picard_link
picard_jar=`pwd`'/picard.jar'
echo '$PICARD="'$picard_jar'"' >> ~/.bashrc


sudo apt-get -y install python3-pip
pip3 install astair


sudo reboot
