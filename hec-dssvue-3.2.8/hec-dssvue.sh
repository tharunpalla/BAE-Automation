#!/bin/bash
#

# If a python script is passed as an arg, start Xvfb and set DISPLAY to run in headless mode
if [ $# -ne 0 ]
then
	if [[ "$1" =~ "*.py" ]]
	then
		unset DISPLAY
		XvfbRunning=`ps -ef | grep Xvfb | grep -v grep | wc -l | sed -e "s/ //g"`
		# start Xfvb if this is not running
		if [ $XvfbRunning -eq 0 ]
		then
			printf "\nStarting Xvfb...\n\n"
			Xvfb :99 -ac -screen 0 1280x1024x8 &
			sleep 5
		fi
		XvfbRunning=`ps -ef | grep Xvfb | grep -v grep | wc -l | sed -e "s/ //g"`
		if [ $XvfbRunning -gt 0 ]
		then
			DISPLAY=":99.0"
			export DISPLAY
		else
			printf "Virtual display server is not running.\n"
			printf "Set DISPLAY variable or start Xvfb.\n"
			exit
		fi
	fi
fi
if [ -z "$DISPLAY" ]; then
        printf "\nThe DISPLAY variable is not set, and no script was passed to HEC-DSSVue. There is nothing to do.\n\n"
        exit
fi

#
# PROG_ROOT=/usr/local/hec/hec-dssvue
PROG_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
JAVA_EXE=$PROG_ROOT/java/jre/bin/java
JARDIR=$PROG_ROOT/jar
JARDIRSYS=$PROG_ROOT/jar/sys
JARDIRHELP=$PROG_ROOT/jar/help

APPDATA=`echo ~/.hec/hec-dssvue`
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${PROG_ROOT}/lib
echo "path "
echo $LD_LIBRARY_PATH
$JAVA_EXE \
-ms64M \
-mx1024M \
-DLOGFILE=$APPDATA/logs/hec-dssvue.log \
-Dpython.path=$PROG_ROOT/jar/sys/jythonlib.jar/lib:jar/sys/jythonUtils.jar \
-Dpython.home=$APPDATA/pythonHome \
-Dlogin.properties.path=$APPDATA/config/login.properties \
-Djava.library.path=$PROG_ROOT/lib \
-Dproperties.path=$PROG_ROOT/config \
-DPLUGINS=$JARDIR/ext \
-DCWMS_HOME=$APPDATA \
-DCWMS_EXE=$PROG_ROOT \
-Djava.security.policy=$PROG_ROOT/config/java.policy \
-cp $JARDIR/*:$JARDIRSYS/*:$JARDIRHELP/*:$JARDIR/ext/* \
hec.dssgui.HecDssVue $* \


