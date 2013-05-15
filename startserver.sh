#!/bin/bash

# Replace these three settings.
PROJDIR=$PWD
PIDFILE="$PROJDIR/everest.pid"

if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

export EVEREST_CONFIG=production.cfg
exec uwsgi -s 127.0.0.1:49152 -w everest:app --daemonize /var/log/uwsgi/everest.log --pidfile $PIDFILE
