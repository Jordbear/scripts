#!/bin/bash
trimmomatic_link=http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.39.zip
picard_link=https://github.com/broadinstitute/picard/releases/download/2.23.3/picard.jar
bedtools_link=https://github.com/arq5x/bedtools2/releases/download/v2.29.2/bedtools.static.binary


sudo apt-get -y update
sudo apt-get -y upgrade

sudo apt-get install -y openjdk-11-jdk

mkdir ~/seq_tools
cd ~/seq_tools

wget $trimmomatic_link
timmomatic_compressed=${trimmomatic_link##*/}
sudo apt-get install -y unzip
unzip $timmomatic_compressed
rm $timmomatic_compressed
trimmomatic=${timmomatic_compressed%%.zip}
trimmomatic_jar=`pwd`'/'$trimmomatic'/'${trimmomatic/T/t}'.jar'
echo 'TRIMMOMATIC='$trimmomatic_jar >> ~/.bashrc

sudo apt-get -y install bwa

sudo apt-get -y install samtools

wget $picard_link
picard_jar=`pwd`'/picard.jar'
echo 'PICARD='$picard_jar >> ~/.bashrc

wget $bedtools_link
chmod u+x bedtools.static.binary
wait
mv bedtools.static.binary ~/.local/bin/bedtools

sudo apt-get -y install python3-pip
pip3 install astair


sudo reboot
