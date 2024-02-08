# Inception Home Alarm Notifier

This is a simple python script that polls an Inception home alarm system for events and if a "Siren Activated" event has been triggered, a notification is sent to all users subscribed to a Telegram bot.

# Installation
```
cd /opt
git clone git@github.com:woodsaj/inception_alarm_bot.git
cd inception_alarm_bot
cp inception_alarm_bot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable inception_alarm_bot.service
```

The service will then start when the machine it is on next starts.  To start immediately, after configuring run
```
systemctl start inception_alarm_bot.service
```


## Configuration
Configure the service by setting the values in the /opt/home-alarm/conf/home-alarm.conf file.
To get started, you can copy the example config:
 ```
 cd /opt/inception_alarm_bot/conf/
 cp inception_alarm_bot.conf.example inception_alarm_bot.conf
 ```

The configuration file should contain the following.
```
# 'USER API Token' configured within the Inception web portal for a user.
INCEPTION_API_KEY=XXX
# IP address of your local Inception system
INCEPTION_ADDR=192.168.100.4

# Telegram bot token and bot name.  use '@BoTFather' to create one if needed.
TELEGRAM_BOT_TOKEN=xxxxx
TELEGRAM_BOT_NAME=your_bot_name_bot

# how frequently (in seconds) to poll the Inception API for new events.
POLL_INTERVAL=30
```

## 