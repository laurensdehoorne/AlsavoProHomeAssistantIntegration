from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass
)

from . import AlsavoProDataCoordinator
from .const import (
    DOMAIN
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)


async def async_setup_entry(hass, entry, async_add_devices):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Water In",
                            "°C",
                            16,
                            False,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Water Out",
                            "°C",
                            17,
                            False,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Ambient",
                            "°C",
                            18,
                            False,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Cold pipe",
                            "°C",
                            19,
                            False,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "heating pipe",
                            "°C",
                            20,
                            False,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "IPM module",
                            "°C",
                            21,
                            False,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Exhaust temperature",
                            "°C",
                            23,
                            False,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Heating mode target",
                            "°C",
                            1,
                            True,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Cooling mode target",
                            "°C",
                            2,
                            True,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Auto mode target",
                            "°C",
                            3,
                            True,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            None,
                            "Fan speed",
                            "RPM",
                            22,
                            False,
                            "mdi:fan"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.CURRENT,
                            "Compressor",
                            "A",
                            26,
                            False,
                            "mdi:current-ac"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.FREQUENCY,
                            "Compressor running frequency",
                            "Hz",
                            27,
                            False,
                            "mdi:air-conditioner"),
            AlsavoProSensor(coordinator,
                            None,
                            "Frequency limit code",
                            "",
                            34,
                            False,
                            "mdi:bell-alert"),
            AlsavoProSensor(coordinator,
                            None,
                            "Alarm code 1",
                            "",
                            48,
                            False,
                            "mdi:bell-alert"),
            AlsavoProSensor(coordinator,
                            None,
                            "Alarm code 2",
                            "",
                            49,
                            False,
                            "mdi:bell-alert"),
            AlsavoProSensor(coordinator,
                            None,
                            "Alarm code 3",
                            "",
                            50,
                            False,
                            "mdi:bell-alert"),
            AlsavoProSensor(coordinator,
                            None,
                            "Alarm code 4",
                            "",
                            51,
                            False,
                            "mdi:bell-alert"),
            AlsavoProSensor(coordinator,
                            None,
                            "Alarm code 4",
                            "",
                            51,
                            False,
                            "mdi:bell-alert"),
            AlsavoProSensor(coordinator,
                            None,
                            "System status code",
                            "",
                            52,
                            False,
                            "mdi:state-machine"),
            AlsavoProSensor(coordinator,
                            None,
                            "System running code",
                            "",
                            53,
                            False,
                            "mdi:state-machine"),
            AlsavoProSensor(coordinator,
                            None,
                            "Device type",
                            "",
                            64,
                            False,
                            "mdi:heat-pump"),
            AlsavoProSensor(coordinator,
                            None,
                            "Main board HW revision",
                            "",
                            65,
                            False,
                            "mdi:heat-pump"),
            AlsavoProSensor(coordinator,
                            None,
                            "Main board SW revision",
                            "",
                            66,
                            False,
                            "mdi:heat-pump"),
            AlsavoProSensor(coordinator,
                            None,
                            "Manual HW code",
                            "",
                            67,
                            False,
                            "mdi:heat-pump"),
            AlsavoProSensor(coordinator,
                            None,
                            "Manual SW code",
                            "",
                            68,
                            False,
                            "mdi:heat-pump"),
            AlsavoProSensor(coordinator,
                            None,
                            "Power mode",
                            "",
                            16,
                            True,
                            "mdi:heat-pump"),
            AlsavoProErrorSensor(coordinator,
                                 "Error messages"),
        ]
    )


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

        self._attr_name = f"{DOMAIN}_{self._data_handler.name}_{name}"
        self._attr_unique_id = f"{self._data_handler.unique_id}_{name}"

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success and self.coordinator.data is not None

    @property
    def native_value(self):
        if not self.available:
            return None

        # Inline implementation of get_temperature_from_status
        def get_temperature_from_status(idx):
            raw = self.coordinator.data.get("status", {}).get(idx)
            if raw is None or raw == 0x7FFF:
                return None
            return round(raw / 10.0, 1)

        # Inline implementation of get_temperature_from_config
        def get_temperature_from_config(idx):
            raw = self.coordinator.data.get("config", {}).get(idx)
            if raw is None or raw == 0x7FFF:
                return None
            return round(raw / 10.0, 1)

        # Inline implementation of get_status_value
        def get_status_value(idx):
            return self.coordinator.data.get("status", {}).get(idx)

        # Inline implementation of get_config_value
        def get_config_value(idx):
            return self.coordinator.data.get("config", {}).get(idx)

        # Determine value based on config/status and data type
        if self._attr_device_class == SensorDeviceClass.TEMPERATURE:
            if self._from_config:
                return get_temperature_from_config(self._data_idx)
            else:
                return get_temperature_from_status(self._data_idx)
        else:
            if self._from_config:
                return get_config_value(self._data_idx)
            else:
                return get_status_value(self._data_idx)



class AlsavoProErrorSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: AlsavoProDataCoordinator, name: str):
        super().__init__(coordinator)
        self.data_coordinator = coordinator
        self._name = name
        self._icon = "mdi:alert"
        self._data_handler = self.data_coordinator.data_handler

    @property
    def name(self):
        return f"{DOMAIN}_{self._data_handler.name}_{self._name}"

    @property
    def unique_id(self):
        return f"{self._data_handler.unique_id}_{self._name}"

    @property
    def available(self) -> bool:
        return self._data_handler.is_online

    @property
    def native_value(self):
        status = self.data_coordinator.data.get("status", {})
        errors = []
        for i in range(48, 52):  # Error code indexes: 48, 49, 50, 51
            code = status.get(i)
            if code is not None and code != 0:
                errors.append(f"E{i - 47}: {code}")
        return ", ".join(errors) if errors else "No errors"

    @property
    def icon(self):
        return self._icon

    async def async_update(self):
        self._data_handler = self.data_coordinator.data_handler

