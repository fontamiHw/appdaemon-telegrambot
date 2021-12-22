# appdaemon-telegrambot

Simple bot to control your home-assistant via a telegram chatbot.
As a requirement, the telegram platform has to be configured in home-assistant (https://www.home-assistant.io/components/notify.telegram/).

Currently the bot provides a simple request/response command interface. The following commands are available:
* /help: Help
* /state_cover: State of cover
* /state_vacuum: State of vacuum
* /state_light: State of light
* /state_climate: State of climate
* /state_person: State of person
* /open_cover: Open cover
* /close_cover: Close cover
* /turnoff_light: Turn off light
* /turnon_light: Turn on light
* /start_vacuum: Start vacuum
* /stop_vacuum: Stop running vacuum
* /restart_hass: Restart hass
* /state_system: State of home-assistant
* /state_sensor: State of sensors
* /get_version: Get version of telegrambot
* /turnon_automation: Turn on automation
* /turnoff_automation: Turn off automation
* /trigger_automation: Trigger automation
* /state_automation: State of automation
* send location message from telegram: for each defined zone in home-assistant the travel time from the current location sent is computed

## Configuration
### appdaemon configuration
1: Just copy the following files to your /appdaemon/apps dir.
* TelegramBot.py
* Helper.py
* conftest.py
* poetry.lock
* pyproject.toml

2: Copy the following folders to your /appdaemon/apps dir:
* images
* helper

3: Get Helper.py from https://github.com/foxcris/appdaemon-helper and copy it to /appdaemon/apps/helper dir.

4: to your apps folder of appaemon and add the following configuration to your apps.yaml (example data shown for some parameters)
```

Helper:
  module: Helper
  class: BaseClass

TelegramBot:
  module:                   TelegramBot
  class:                    TelegramBot
  debug:                    True
  extend_system:            sensor.date,sensor.heartbeat
  extend_light
  filter_blacklist:
  filter_whitelist:
    - sample
  routing:
    waze:
      region:               EU
      avoid_toll_roads:     True
  hass:
    token: !secret ha_token
    ha_url: http://hass:8123
  ```

||Configuration parameter || Description ||
* |extend_system | comma separated list of complete entities to include in the system report|
* |extend_light | comma separated list of complete entities to include in the commands /state_light /turnoff_light /turnon_light|
* |filter_blacklist| python regex to exclude entities from being reported/used from telegrambot|
* |filter_whitelist| python regex to whitelist entities from being reported/used from telegrambot|
* The following logic is used to apply the blacklist and whitelist:
- If the blacklist is empty - nothing is filtered out
- If the whitelist is empty - nothing is filtered out
- If both the blacklist and whitelist are non-empty, first the blacklist ist applied and then the whitelist|
* |routing| currently only waze is supported. region can be 'US','EU','IL','AU' and is used to select the correct routingserver from waze. avoid_toll_roads is a boolean to enable/disable the use of toll roads in the travel time computation.|
* |hass| the url and port of home assisstant, for example http://192.168.1.31:8123. The ha_token is a long-lived access token you have to create for the plugin to communicate with HA. You can create it in HA in the administrator section of HA (login to admin account, than in the left pane the lowest button: administrator, scroll to bottom: long-live acces token).

The file Helper.py is also used by one of my [other](https://github.com/foxcris/appdaemon-blinds-control) appdaemon project. In both projects the same file is used!

## Screenshots
<img src="https://raw.githubusercontent.com/foxcris/appdaemon-telegrambot/master/images/Screenshot_20190310_123130_org.telegram.messenger.jpg" width="250">
<img src="https://raw.githubusercontent.com/foxcris/appdaemon-telegrambot/master/images/Screenshot_20190403_210457_org.telegram.messenger.jpg" width="250">
<img src="https://raw.githubusercontent.com/foxcris/appdaemon-telegrambot/master/images/Screenshot_20190403_210508_org.telegram.messenger.jpg" width="250">
<img src="https://raw.githubusercontent.com/foxcris/appdaemon-telegrambot/master/images/Screenshot_20190403_210559_org.telegram.messenger.jpg" width="250">

## Contributing

* All contributions are welcome!
* A PR must be accompanied with some tests for the new feature
* Please take care that:
  * The code is readable and is optimally documented
  * The code passes all tests

### Tests

For the unit test the [Appdamon-Test-Framework](https://github.com/FlorianKempenich/Appdaemon-Test-Framework) is used together with [pytest](https://docs.pytest.org/en/latest/).

### Requirements

All necessary requirements are listed in the `pyproject.toml`.
