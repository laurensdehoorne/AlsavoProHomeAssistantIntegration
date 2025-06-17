from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass
)

from . import AlsavoProDataCoordinator
from .const import DOMAIN
from homeassistant.helpers.update_coordinator import CoordinatorEntity


async def async_setup_entry(hass, entry, async_add_devices):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        AlsavoProSensor(coordinator, SensorDeviceClass.TEMPERATURE, "Water In", "°C", 16, False, "mdi:thermometer"),
        AlsavoProSensor(coordinator, SensorDeviceClass.TEMPERATURE, "Water Out", "°C", 17, False, "mdi:thermometer"),
        AlsavoProSensor(coordinator, SensorDeviceClass.TEMPERATURE, "Ambient", "°C", 18, False, "mdi:thermometer"),
        AlsavoProSensor(coordinator, SensorDeviceClass.TEMPERATURE, "Cold pipe", "°C", 19, False, "mdi:thermometer"),
        AlsavoProSensor(coordinator, SensorDeviceClass.TEMPERATURE, "Heating pipe", "°C", 20, False, "mdi:thermometer"),
        AlsavoProSensor(coordinator, SensorDeviceClass.TEMPERATURE, "IPM module", "°C", 21, False, "mdi:thermometer"),
        AlsavoProSensor(coordinator, SensorDeviceClass.TEMPERATURE, "Exhaust temperature", "°C", 23, False, "mdi:thermometer"),
        AlsavoProSensor(coordinator, SensorDeviceClass.TEMPERATURE, "Heating mode target", "°C", 1, True, "mdi:thermometer"),
        AlsavoProSensor(coordinator, SensorDeviceClass.TEMPERATURE, "Cooling mode target", "°C", 2, True, "mdi:thermometer"),
        AlsavoProSensor(coordinator, SensorDeviceClass.TEMPERATURE, "Auto mode target", "°C", 3, True, "mdi:thermometer"),
        AlsavoProSensor(coordinator, None, "Fan speed", "RPM", 22, False, "mdi:fan"),
        AlsavoProSensor(coordinator, SensorDeviceClass.CURRENT, "Compressor", "A", 26, False, "mdi:current-ac"),
        AlsavoProSensor(coordinator, SensorDeviceClass.FREQUENCY, "Compressor running frequency", "Hz", 27, False, "mdi:air-conditioner"),
        AlsavoProSensor(coordinator, None, "Frequency limit code", "", 34, False, "mdi:bell-alert"),
        AlsavoProSensor(coordinator, None, "Alarm code 1", "", 48, False, "mdi:bell-alert"),
        AlsavoProSensor(coordinator, None, "Alarm code 2", "", 49, False, "mdi:bell-alert"),
        AlsavoProSensor(coordinator, None, "Alarm code 3", "", 50, False, "mdi:bell-alert"),
        AlsavoProSensor(coordinator, None, "Alarm code 4", "", 51, False, "mdi:bell-alert"),
        AlsavoProSensor(coordinator, None, "System status code", "", 52, False, "mdi:state-machine"),
        AlsavoProSensor(coordinator, None, "System running code", "", 53, False, "mdi:state-machine"),
        AlsavoProSensor(coordinator, None, "Device type", "", 64, False, "mdi:heat-pump"),
        AlsavoProSensor(coordinator, None, "Main board HW revision", "", 65, False, "mdi:heat-pump"),
        AlsavoProSensor(coordinator, None, "Main board SW revision", "", 66, False, "mdi:heat-pump"),
        AlsavoProSensor(coordinator, None, "Manual HW code", "", 67, False, "mdi:heat-pump"),
        AlsavoProSensor(coordinator, None, "Manual SW code", "", 68, False, "mdi:heat-pump"),
        AlsavoProSensor(coordinator, None, "Power mode", "", 16, True, "mdi:heat-pump"),
        AlsavoProErrorSensor(coordinator, "Error messages"),
    ]

    async_add_devices(sensors)


class AlsavoProSensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator: AlsavoProDataCoordinator,
        device_class: SensorDeviceClass,
        name: str,
        unit: str,
        idx: int,
        from_config: bool,
        icon: str,
    ):
        super().__init__(coordinator)
        self._data_handler = coordinator.data_handler
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._data_idx = idx
        self._from_config = from_config
        self._name = name

        slug_name = name.lower().replace(" ", "_")
        self._attr_name = f"{DOMAIN}_{self._data_handler.name}_{name}"
        self._attr_unique_id = f"{self._data_handler.unique_id}_{slug_name}_{idx}"

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success and self._data_handler.is_online

    @property
    def native_value(self):
        if not self.available:
            return None

        def get_temperature(raw):
            if raw is None or raw == 0x7FFF:
                return None
            return round(raw / 10.0, 1)

        try:
            if self._from_config:
                raw = self._data_handler.get_config_value(self._data_idx)
            else:
                raw = self._data_handler.get_status_value(self._data_idx)

            if self._attr_device_class == SensorDeviceClass.TEMPERATURE:
                return get_temperature(raw)
            return raw

        except Exception:
            return None


class AlsavoProErrorSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: AlsavoProDataCoordinator, name: str):
        super().__init__(coordinator)
        self._data_handler = coordinator.data_handler
        self._name = name
        self._attr_icon = "mdi:alert"
        self._attr_name = f"{DOMAIN}_{self._data_handler.name}_{name}"
        self._attr_unique_id = f"{self._data_handler.unique_id}_{name.lower().replace(' ', '_')}"

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success and self._data_handler.is_online

    @property
    def native_value(self):
        if not self.available:
            return None

        errors = []
        try:
            for i in range(48, 52):
                code = self._data_handler.get_status_value(i)
                if code and code != 0:
                    errors.append(f"E{i - 47}: {code}")
        except Exception:
            return None

        return ", ".join(errors) if errors else "No errors"
