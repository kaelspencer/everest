#!/bin/bash

. ../virtualenv/everest/bin/activate

export EVEREST_CONFIG=production.cfg
exec uwsgi -s 127.0.0.1:49152 --module everest --callable app --logto /var/log/uwsgi/everest.log
