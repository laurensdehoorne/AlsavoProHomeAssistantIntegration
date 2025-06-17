"""Support for Alsavo Pro wifi-enabled pool heaters."""
import logging

from homeassistant.components.climate import (
    PLATFORM_SCHEMA,
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode
)

from homeassistant.const import (
    ATTR_TEMPERATURE,
    CONF_PASSWORD,
    CONF_IP_ADDRESS,
    CONF_PORT,
    CONF_NAME,
    PRECISION_TENTHS,
    UnitOfTemperature,
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from . import AlsavoProDataCoordinator
from .const import (
    DOMAIN,
    POWER_MODE_MAP
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([AlsavoProClimate(hass.data[DOMAIN][entry.entry_id])])


class AlsavoProClimate(CoordinatorEntity, ClimateEntity):
    """Climate platform for Alsavo Pro pool heater."""

    def __init__(self, coordinator: AlsavoProDataCoordinator):
        super().__init__(coordinator)
        self._data_handler = coordinator.data_handler
        self._attr_unique_id = self._data_handler.unique_id
        self._attr_name = self._data_handler.name

    @property
    def supported_features(self):
        return ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success and self.coordinator.data is not None

    @property
    def hvac_mode(self):
        if not self.coordinator.data["is_power_on"]:
            return HVACMode.OFF

        return {
            0: HVACMode.COOL,
            1: HVACMode.HEAT,
            2: HVACMode.AUTO,
        }.get(self.coordinator.data["operating_mode"], HVACMode.AUTO)

    @property
    def hvac_modes(self):
        return [HVACMode.HEAT, HVACMode.COOL, HVACMode.AUTO, HVACMode.OFF]

    @property
    def preset_mode(self):
        return POWER_MODE_MAP.get(self.coordinator.data["power_mode"])

    @property
    def preset_modes(self):
        return ["Silent", "Smart", "Powerful"]

    @property
    def icon(self):
        return {
            HVACMode.HEAT: "mdi:fire",
            HVACMode.COOL: "mdi:snowflake",
            HVACMode.AUTO: "mdi:refresh-auto",
        }.get(self.hvac_mode, "mdi:hvac-off")

    @property
    def temperature_unit(self):
        return UnitOfTemperature.CELSIUS

    @property
    def min_temp(self):
        return self.coordinator.data["min_temp"]

    @property
    def max_temp(self):
        return self.coordinator.data["max_temp"]

    @property
    def current_temperature(self):
        return self.coordinator.data["water_in_temperature"]

    @property
    def target_temperature(self):
        return self.coordinator.data["target_temperature"]

    @property
    def target_temperature_step(self):
        return PRECISION_TENTHS

    async def async_set_temperature(self, **kwargs):
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        await self._data_handler.set_target_temperature(temperature)
        await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode):
        actions = {
            HVACMode.OFF: self._data_handler.set_power_off,
            HVACMode.COOL: self._data_handler.set_cooling_mode,
            HVACMode.HEAT: self._data_handler.set_heating_mode,
            HVACMode.AUTO: self._data_handler.set_auto_mode,
        }
        action = actions.get(hvac_mode)
        if action:
            await action()
            await self.coordinator.async_request_refresh()

    async def async_set_preset_mode(self, preset_mode):
        modes = {
            "Silent": 0,
            "Smart": 1,
            "Powerful": 2,
        }
        power_mode = modes.get(preset_mode)
        if power_mode is not None:
            await self._data_handler.set_power_mode(power_mode)
            await self.coordinator.async_request_refresh()

    async def async_update(self):
        await self.coordinator.async_request_refresh()
