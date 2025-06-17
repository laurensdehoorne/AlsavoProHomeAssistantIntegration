"""Alsavo Pro pool heat pump integration."""
import logging
from datetime import timedelta

import async_timeout
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_IP_ADDRESS,
    CONF_PORT,
    CONF_NAME,
)

from .AlsavoPyCtrl import AlsavoPro
from .const import (
    DOMAIN,
    SERIAL_NO,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    return True


async def async_setup_entry(hass, entry):
    """Set up the Alsavo Pro heater from a config entry."""
    name = entry.data.get(CONF_NAME)
    serial_no = entry.data.get(SERIAL_NO)
    ip_address = entry.data.get(CONF_IP_ADDRESS)
    port_no = entry.data.get(CONF_PORT)
    password = entry.data.get(CONF_PASSWORD)

    data_handler = AlsavoPro(name, serial_no, ip_address, port_no, password)

    try:
        await data_handler.update()
    except Exception as ex:
        _LOGGER.exception("Initial connection to Alsavo Pro failed: %s", ex)
        return False

    data_coordinator = AlsavoProDataCoordinator(hass, data_handler)

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    hass.data[DOMAIN][entry.entry_id] = data_coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "climate"])

    return True


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, ["climate", "sensor"]
    )
    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id, None)
    return unload_ok


class AlsavoProDataCoordinator(DataUpdateCoordinator):
    """Data coordinator for Alsavo Pro."""

    def __init__(self, hass, data_handler):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="AlsavoPro",
            update_interval=timedelta(seconds=15),
        )
        self.data_handler = data_handler

    async def _async_update_data(self):
    _LOGGER.debug("_async_update_data")
    try:
        async with async_timeout.timeout(10):
            await self.data_handler.update()
            if self.data_handler.is_online:
                return self.data_handler
            raise UpdateFailed("Device offline or returned no data")
    except Exception as ex:
        _LOGGER.error(f"_async_update_data failed: {ex}")
        raise UpdateFailed(f"Update failed: {ex}") from ex

