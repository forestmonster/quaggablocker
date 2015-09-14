#!/bin/sh
# FreeBSD startup script for AutoRTBH

# REQUIRE: quagga

. /etc/rc.d/subr

name="quaggablocker"
rcvar="quaggablocker_enable"
command_interpreter="/usr/local/bin/python"
pidfile="/var/run/${name}.pid"
# Correct this variable for your environment.
start_precmd="EXPORT BHR_HOST=https://127.0.0.1:8000; EXPORT BHR_IDENT=quagga; EXPORT BHR_TOKEN=db4de92f933092b1f1f6665a742b7192a5eced77" 
command="/usr/local/sbin/quaggablocker.py"

load_rc_config $name
run_rc_command "$1"
