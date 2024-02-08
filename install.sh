#!/usr/bin/env bash

set -e

cd /opt/inception_alarm_bot
cp inception_alarm_bot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable inception_alarm_bot.service

chown -R daemon /opt/inception_alarm_bot/run

