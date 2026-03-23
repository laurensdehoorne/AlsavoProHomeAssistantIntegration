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
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Compressor input temperature",
                            "°C",
                            24,
                            False,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            None,
                            "EEV opening",
                            "",
                            25,
                            False,
                            "mdi:valve"),
            AlsavoProSensor(coordinator,
                            None,
                            "Compressor speed setting",
                            "",
                            33,
                            False,
                            "mdi:speedometer"),
            AlsavoProSensor(coordinator,
                            None,
                            "Device status code",
                            "",
                            54,
                            False,
                            "mdi:state-machine"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Heating max temperature",
                            "°C",
                            55,
                            False,
                            "mdi:thermometer-high"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Cooling min temperature",
                            "°C",
                            56,
                            False,
                            "mdi:thermometer-low"),
            AlsavoProSensor(coordinator,
                            None,
                            "Manual frequency setting",
                            "",
                            6,
                            True,
                            "mdi:sine-wave"),
            AlsavoProSensor(coordinator,
                            None,
                            "Manual EEV setting",
                            "",
                            7,
                            True,
                            "mdi:valve"),
            AlsavoProSensor(coordinator,
                            None,
                            "Manual fan speed setting",
                            "",
                            8,
                            True,
                            "mdi:fan"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Defrost in temperature",
                            "°C",
                            9,
                            True,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Defrost out temperature",
                            "°C",
                            10,
                            True,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            SensorDeviceClass.TEMPERATURE,
                            "Water temperature calibration",
                            "°C",
                            11,
                            True,
                            "mdi:thermometer"),
            AlsavoProSensor(coordinator,
                            None,
                            "Defrost in time",
                            "min",
                            12,
                            True,
                            "mdi:timer"),
            AlsavoProSensor(coordinator,
                            None,
                            "Defrost out time",
                            "min",
                            13,
                            True,
                            "mdi:timer"),
            AlsavoProSensor(coordinator,
                            None,
                            "Hot over",
                            "",
                            14,
                            True,
                            "mdi:thermometer-high"),
            AlsavoProSensor(coordinator,
                            None,
                            "Cold over",
                            "",
                            15,
                            True,
                            "mdi:thermometer-low"),
            AlsavoProSensor(coordinator,
                            None,
                            "Unknown config 17",
                            "",
                            17,
                            True,
                            "mdi:help-circle"),
            AlsavoProSensor(coordinator,
                            None,
                            "Current time",
                            "",
                            32,
                            True,
                            "mdi:clock"),
            AlsavoProSensor(coordinator,
                            None,
                            "Timer on time",
                            "",
                            33,
                            True,
                            "mdi:timer"),
            AlsavoProSensor(coordinator,
                            None,
                            "Timer off time",
                            "",
                            34,
                            True,
                            "mdi:timer"),
            AlsavoProErrorSensor(coordinator,
                                 "Error messages"),
        ]
    )


class AlsavoProSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: AlsavoProDataCoordinator,
                 device_class: SensorDeviceClass,
                 name: str,
                 unit: str,
                 idx: int,
                 from_config: bool,
                 icon: str):
        super().__init__(coordinator)
        self.data_coordinator = coordinator
        self._data_handler = self.data_coordinator.data_handler
        self._name = name
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._dataIdx = idx
        self._config = from_config
        self._icon = icon

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DOMAIN}_{self._data_handler.name}_{self._name}"

    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will reflect this.
    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return self._data_handler.is_online

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._data_handler.unique_id}_{self._name}"

    @property
    def native_value(self):
        # Hent data fra data_handler her
        if self._attr_device_class == SensorDeviceClass.TEMPERATURE:
            if self._config:
                return self._data_handler.get_temperature_from_config(self._dataIdx)
            else:
                return self._data_handler.get_temperature_from_status(self._dataIdx)
        else:
            if self._config:
                return self._data_handler.get_config_value(self._dataIdx)
            else:
                return self._data_handler.get_status_value(self._dataIdx)

    @property
    def icon(self):
        return self._icon


class AlsavoProErrorSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: AlsavoProDataCoordinator,
                 name: str):
        super().__init__(coordinator)
        self.data_coordinator = coordinator
        self._data_handler = self.data_coordinator.data_handler
        self._name = name
        self._icon = "mdi:alert"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DOMAIN}_{self._data_handler.name}_{self._name}"

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._data_handler.unique_id}_{self._name}"

    @property
    def native_value(self):
        return self._data_handler.errors

    @property
    def icon(self):
        return self._icon

    async def async_update(self):
        """Get the latest data."""
        self._data_handler = self.data_coordinator.data_handler
