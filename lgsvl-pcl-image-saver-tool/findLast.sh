#! /bin/bash
cd ~/spark/lgsvlsimulator
dir=$(pwd)

if [ ! -d "$dir/$1" ]

then
	mkdir ~/spark/lgsvlsimulator/$1
	last=0
else
	if [[ $(ls -A ~/spark/lgsvlsimulator/$1) ]]; then
		last_file=$(ls -t ~/spark/lgsvlsimulator/camera | head -n 1)
		last=$(echo $last_file | sed -E 's/(camera|lidar)([0-9]+).*/\2/g')

	else
		last=0
	fi
fi

echo $last

