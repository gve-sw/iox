#!/bin/sh
PWD=`pwd`
DIR=$PWD"/gwaas_sensehat_pkg"

if [ ! -d "$DIR" ]; then
	    mkdir $DIR
    else
	        rm -rf $DIR/*
	fi

	echo "Preparing $DIR folder...."
        cp -f $PWD/device_mapping.json $DIR/
        cp -f $PWD/main.py $DIR/
        cp -f $PWD/package_config.ini $DIR/
        cp -f $PWD/package.yaml $DIR/
        cp -f $PWD/requirements.txt $DIR/
        cp -f $PWD/sensor_data.py $DIR/
        cp -f $PWD/STAR_iotspdev_io.crt $DIR/
        cp -f $PWD/start.sh $DIR/

	echo "Building package.tar.gz"
	ioxclient package $DIR/
