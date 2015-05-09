#! /bin/sh

/etc/init.d/controlCamera.sh start
/etc/init.d/controlRequests.sh start
/etc/init.d/controlRequestPhoto.sh start
/etc/init.d/controlGPS.sh start
/etc/init.d/controlWIFI.sh start


while true
do
	/etc/init.d/controlCamera.sh status
	statusCamera="$?"
	echo "StatusCamera" "$statusCamera" 
	if [ $statusCamera -ne 0 ]; then
		/etc/init.d/controlCamera.sh restart
	fi

	/etc/init.d/controlRequests.sh status
	statusRequests="$?"
	echo "StatusRequest" "$statusRequests" 
	if [ $statusRequests -ne 0 ]; then
		/etc/init.d/controlRequests.sh restart
	fi

	/etc/init.d/controlRequestPhoto.sh status
	statusRequestPhoto="$?"
	echo "StatusRequestPhoto" "$statusRequestPhoto" 
	if [ $statusRequestPhoto -ne 0 ]; then
		/etc/init.d/controlRequestPhoto.sh restart
	fi

	/etc/init.d/controlGPS.sh status
	statusGPS="$?"
	echo "StatusGPS" "$statusGPS" 
	if [ $statusGPS -ne 0 ]; then
		/etc/init.d/controlGPS.sh restart
	fi

	/etc/init.d/controlWIFI.sh status
	statusWIFI="$?"
	echo "StatusWIFI" "$statusWIFI" 
	if [ $statusWIFI -ne 0 ]; then
		/etc/init.d/controlWIFI.sh restart
	fi


done
