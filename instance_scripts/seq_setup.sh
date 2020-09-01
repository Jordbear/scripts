#!/bin/bash
fastqc_link=https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.9.zip
trimmomatic_link=http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.39.zip
picard_link=https://github.com/broadinstitute/picard/releases/download/2.23.3/picard.jar
bedtools_link=https://github.com/arq5x/bedtools2/releases/download/v2.29.2/bedtools.static.binary
trimgalore_link=https://github.com/FelixKrueger/TrimGalore/archive/0.6.5.tar.gz
bamutil_link=https://github.com/statgen/bamUtil/archive/v1.0.14.tar.gz


sudo apt-get -y update
sudo apt-get -y upgrade

sudo apt-get install -y openjdk-11-jdk
sudo apt-get install -y unzip
sudo apt-get -y install python3-pip

mkdir ~/seq_tools
cd ~/seq_tools

wget $fastqc_link
fastqc_compressed=${fastqc_link##*/}
unzip $fastqc_compressed
rm $fastqc_compressed
fastqc_dir=`pwd`'/FastQC'
chmod u+x $fastqc_dir'/fastqc'
echo 'PATH=$PATH:'$fastqc_dir >> ~/.profile

wget $trimmomatic_link
timmomatic_compressed=${trimmomatic_link##*/}
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
sudo mv bedtools.static.binary /usr/local/bin/bedtools

pip3 install astair

pip3 install cutadapt
echo 'PATH=$PATH:~/.local/bin' >> ~/.profile
wget $trimgalore_link
trimgalore_compressed=${trimgalore_link##*/}
tar -xvf ${trimgalore_compressed}
rm ${trimgalore_compressed}
trimgalore=${trimgalore_compressed%%.tar.gz}
trimgalore_dir=`pwd`'/TrimGalore-'$trimgalore
echo 'PATH=$PATH:'$trimgalore_dir >> ~/.profile
sudo apt-get install -y pigz

wget $bamutil_link
bamutil_compressed=${bamutil_link##*/}
tar -xvf ${bamutil_compressed}
rm ${bamutil_compressed}
bamutil_version=${bamutil_compressed%%.tar.gz}
bamutil_dir='bamUtil-'${bamutil_version#v}
cd $bamutil_dir
make cloneLib
make
sudo make install
cd ..



sudo reboot
