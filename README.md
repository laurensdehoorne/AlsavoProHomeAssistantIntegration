# Alsavo Pro / Swim & Fun / Artic Pro / Zealux ++ pool heatpump

Custom component for controlling pool heatpumps that uses the Alsavo Pro app in Home Assistant.

## Install
#### Manually
In Home Assistant, create a folder under *custom_components* named *AlsavoPro* and copy all the content of this project to that folder.
Restart Home Assistant and go to *Devices and Services* and press *+Add integration*.
Search for *AlsavoPro* and add it.
#### HACS Custom Repository
In HACS, add a custom repository and use https://github.com/laurensdehoorne/AlsavoProHomeAssistantIntegration
Download from HACS.
Restart Home Assistant and go to *Devices and Services* and press *+Add integration*.
Search for *AlsavoPro* and add it.

## Configuration
You must now choose a name for the device. The serial number for the heat pump can be found in the Alsavo Pro app by logging in to the heat pump and pressing the Alsavo Pro-logo in the upper right corner.
Password is the same as the one you logged into the Alsavo Pro app with.

Ip-address and port can be one of two:
- If you want to use the cloud, set IP-address to 47.254.157.150 and port to 51192.
- If you want to bypass the cloud, enter the heat pumps ip-address and use port 1194.

## Changelog

### 1.0.2
- Fixed `set_config` recursive retry replaced with iterative loop to prevent stack overflow and stale `_online` state
- Fixed `is_online` now correctly reflects live connection state instead of stale data presence
- Fixed `Payload.get_value` off-by-one bounds check

### 1.0.1
- Fixed `NoneType object is not subscriptable` crash when pump is temporarily offline during auth challenge
- Fixed `unpack requires a buffer of X bytes` error when receiving truncated UDP packets
- Added 2-second delay between update retries so the pump has time to recover when briefly offline

## AlsavoCtrl
This code is very much based on AlsavoCtrl: https://github.com/strandborg/AlsavoCtrl
