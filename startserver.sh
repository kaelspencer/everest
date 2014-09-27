#!/bin/bash

# Replace these three settings.
PROJDIR=$PWD
PIDFILE="$PROJDIR/everest.pid"

if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

. ../virtualenv/everest/bin/activate

export EVEREST_CONFIG=production.cfg
exec uwsgi -s 127.0.0.1:49152 --module everest --callable app --daemonize /var/log/uwsgi/everest.log --pidfile $PIDFILE
