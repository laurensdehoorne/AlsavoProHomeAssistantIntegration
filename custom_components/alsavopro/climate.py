"""Support for Alsavo Pro wifi-enabled pool heaters."""
import logging

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    UnitOfTemperature,
    PRECISION_TENTHS,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import AlsavoProDataCoordinator
from .const import DOMAIN, POWER_MODE_MAP

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Alsavo Pro climate entity from config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AlsavoProClimate(coordinator)])


class AlsavoProClimate(CoordinatorEntity, ClimateEntity):
    """Climate platform for Alsavo Pro pool heater."""

    def __init__(self, coordinator: AlsavoProDataCoordinator):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._data_handler = coordinator.data_handler
        self._name = self._data_handler.name

    @property
    def supported_features(self):
        return ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE

    @property
    def unique_id(self):
        return self._data_handler.unique_id

    @property
    def name(self):
        return self._name

    @property
    def available(self) -> bool:
        return self._data_handler.is_online

    @property
    def hvac_mode(self):
        if not self._data_handler.is_power_on:
            return HVACMode.OFF
        return {
            0: HVACMode.COOL,
            1: HVACMode.HEAT,
            2: HVACMode.AUTO
        }.get(self._data_handler.operating_mode, HVACMode.OFF)

    @property
    def hvac_modes(self):
        return [HVACMode.HEAT, HVACMode.COOL, HVACMode.AUTO, HVACMode.OFF]

    @property
    def preset_mode(self):
        return POWER_MODE_MAP.get(self._data_handler.power_mode)

    @property
    def preset_modes(self):
        return list(POWER_MODE_MAP.values())

    @property
    def icon(self):
        return {
            HVACMode.HEAT: "mdi:fire",
            HVACMode.COOL: "mdi:snowflake",
            HVACMode.AUTO: "mdi:refresh-auto",
            HVACMode.OFF: "mdi:hvac-off"
        }.get(self.hvac_mode, "mdi:hvac-off")

    @property
    def temperature_unit(self):
        return UnitOfTemperature.CELSIUS

    @property
    def target_temperature_step(self):
        return PRECISION_TENTHS

    def _get_temperature_from_status(self, idx):
        if not self.coordinator.data or "status" not in self.coordinator.data:
            return None
        raw = self.coordinator.data["status"].get(idx)
        if raw is None or raw == 0x7FFF:
            return None
        return round(raw / 10.0, 1)

    @property
    def min_temp(self):
        return self._get_temperature_from_status(56) or 5.0  # fallback if undefined

    @property
    def max_temp(self):
        return self._get_temperature_from_status(55) or 45.0  # fallback if undefined

    @property
    def current_temperature(self):
        return self._data_handler.water_in_temperature or self._get_temperature_from_status(16)

    @property
    def target_temperature(self):
        return self._data_handler.target_temperature

    async def async_set_hvac_mode(self, hvac_mode):
        _LOGGER.debug("Setting HVAC mode to %s", hvac_mode)
        hvac_mode_actions = {
            HVACMode.OFF: self._data_handler.set_power_off,
            HVACMode.COOL: self._data_handler.set_cooling_mode,
            HVACMode.HEAT: self._data_handler.set_heating_mode,
            HVACMode.AUTO: self._data_handler.set_auto_mode
        }
        action = hvac_mode_actions.get(hvac_mode)
        if action:
            await action()
            await self.coordinator.async_request_refresh()

    async def async_set_preset_mode(self, preset_mode):
        _LOGGER.debug("Setting preset mode to %s", preset_mode)
        preset_to_power_mode = {
            'Silent': 0,
            'Smart': 1,
            'Powerful': 2
        }
        power_mode = preset_to_power_mode.get(preset_mode)
        if power_mode is not None:
            await self._data_handler.set_power_mode(power_mode)
            await self.coordinator.async_request_refresh()

    async def async_set_temperature(self, **kwargs):
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            _LOGGER.warning("No temperature provided to set_temperature")
            return
        _LOGGER.debug("Setting target temperature to %.1f°C", temperature)
        await self._data_handler.set_target_temperature(temperature)
        await self.coordinator.async_request_refresh()

    @property
    def extra_state_attributes(self):
        return {
            "device_power_on": self._data_handler.is_power_on,
            "operating_mode_code": self._data_handler.operating_mode,
            "power_mode_code": self._data_handler.power_mode,
            "device_online": self._data_handler.is_online,
            "target_temp_idx": self._data_handler.target_temperature_idx,
        }
