#!/bin/bash
trimmomatic=http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.39.zip
picard=https://github.com/broadinstitute/picard/archive/2.23.3.tar.gz

sudo apt-get -y update
sudo apt-get -y upgrade

mkdir ~/seq_tools
cd ~/seq_tools

wget $trimmomatic
tar -xzf ${trimmomatic##*/}

sudo apt-get -y bwa

wget $picard
tar -xzf ${picard##*/}
