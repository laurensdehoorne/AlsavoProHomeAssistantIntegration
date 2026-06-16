"""Binary sensors for Alsavo Pro: connectivity, frost protection, alarm."""
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.const import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import AlsavoProDataCoordinator, AlsavoProEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            AlsavoProConnectivitySensor(coordinator),
            AlsavoProFrostProtectionSensor(coordinator),
            AlsavoProAlarmSensor(coordinator),
        ]
    )


class _AlsavoProBinarySensorBase(AlsavoProEntity, CoordinatorEntity, BinarySensorEntity):
    """Shared plumbing for the Alsavo Pro binary sensors."""

    _label = ""
    _key = ""

    def __init__(self, coordinator: AlsavoProDataCoordinator):
        super().__init__(coordinator)
        self.data_coordinator = coordinator
        self._data_handler = coordinator.data_handler

    @property
    def name(self) -> str:
        return f"{DOMAIN}_{self._data_handler.name}_{self._label}"

    @property
    def unique_id(self) -> str:
        return f"{self._data_handler.unique_id}_{self._key}"


class AlsavoProConnectivitySensor(_AlsavoProBinarySensorBase):
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _label = "Connectivity"
    _key = "connectivity"

    @property
    def available(self) -> bool:
        # The connectivity sensor must stay available to report "off" when the
        # pump goes offline — otherwise it would disappear exactly when it
        # carries the most useful information.
        return True

    @property
    def is_on(self) -> bool:
        return self._data_handler.is_online


class AlsavoProFrostProtectionSensor(_AlsavoProBinarySensorBase):
    _attr_device_class = BinarySensorDeviceClass.COLD
    _attr_icon = "mdi:snowflake-alert"
    _label = "Frost protection"
    _key = "frost_protection"

    @property
    def available(self) -> bool:
        return self._data_handler.is_online

    @property
    def is_on(self) -> bool:
        return self._data_handler.is_frost_protection


class AlsavoProAlarmSensor(_AlsavoProBinarySensorBase):
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _label = "Alarm"
    _key = "alarm"

    @property
    def available(self) -> bool:
        return self._data_handler.is_online

    @property
    def is_on(self) -> bool:
        return bool(self._data_handler.errors)

    @property
    def extra_state_attributes(self):
        return {"error_message": self._data_handler.errors}
