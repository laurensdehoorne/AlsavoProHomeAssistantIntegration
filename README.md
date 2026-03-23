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

## Alarm codes

The integration exposes four alarm code sensors (`alarm_code_1` through `alarm_code_4`) that reflect the raw values of the pump's status registers. The `errors` attribute decodes all active alarms into human-readable messages.

### EE codes (Electrical/Component) — registers 48 & 49

| Code | Malfunction |
|------|-------------|
| EE01 | High pressure failure |
| EE02 | Low pressure failure |
| EE03 | Water flow failure |
| EE04 | Water temperature overheating protection (heating mode) |
| EE05 | Exhaust temperature too high |
| EE06 | Controller malfunction or communication failure |
| EE07 | Compressor current protection |
| EE08 | Communication failure (controller ↔ PCB) |
| EE09 | Communication failure (PCB ↔ driver board) |
| EE10 | VDC voltage too high protection |
| EE11 | IPM module protection |
| EE12 | VDC voltage too low protection |
| EE13 | Input current too strong protection |
| EE14 | IPM module thermal circuit abnormal |
| EE15 | IPM module temperature too high protection |
| EE16 | PFC module protection |
| EE17 | DC fan failure |
| EE18 | PFC module thermal circuit abnormal |
| EE19 | PFC module high temperature protection |
| EE20 | Input power failure |
| EE21 | Software control failure |
| EE22 | Current detection circuit failure |
| EE23 | Compressor start failure |
| EE24 | Ambient temperature sensor failure (driving board) |
| EE25 | Compressor phase failure |
| EE26 | 4-way valve reversal failure |
| EE27 | EEPROM data reading failure |
| EE28 | Inter-chip communication failure (main control board) |

### PP codes (Protection/Sensor) — register 50

| Code | Malfunction |
|------|-------------|
| PP01 | Inlet water temperature sensor failure |
| PP02 | Outlet water temperature sensor failure |
| PP03 | Heating coil pipe sensor failure |
| PP04 | Gas return sensor failure |
| PP05 | Ambient temperature sensor failure |
| PP06 | Exhaust temperature sensor failure |
| PP07 | Anti-freezing protection (winter) |
| PP08 | Low ambient temperature protection |
| PP10 | Coil pipe temperature too high protection (cooling mode) |
| PP11 | Water temperature (T2) too low protection (cooling mode) |

## Changelog

### 1.0.3
- Full alarm code decoding for all EE (EE01–EE28) and PP (PP01–PP11) fault codes across registers 48–50

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
