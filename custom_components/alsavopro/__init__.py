"""Alsavo Pro pool heat pump integration."""
from __future__ import annotations

import logging
from datetime import timedelta

import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_IP_ADDRESS,
    CONF_PORT,
    CONF_NAME,
)

from .AlsavoPyCtrl import AlsavoPro
from .const import DOMAIN, SERIAL_NO

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the AlsavoPro component (not using YAML)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AlsavoPro from a config entry."""
    name = entry.data[CONF_NAME]
    serial_no = entry.data[SERIAL_NO]
    ip_address = entry.data[CONF_IP_ADDRESS]
    port_no = entry.data[CONF_PORT]
    password = entry.data[CONF_PASSWORD]

    data_handler = AlsavoPro(name, serial_no, ip_address, port_no, password)

    # First-time fetch to ensure connectivity
    try:
        await data_handler.update()
    except Exception as err:
        _LOGGER.exception("Initial update failed: %s", err)
        raise ConfigEntryNotReady from err

    coordinator = AlsavoProDataCoordinator(hass, data_handler)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ("sensor", "climate"))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ("sensor", "climate"))
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok


class AlsavoProDataCoordinator(DataUpdateCoordinator[dict]):
    """Class to manage fetching Alsavo Pro data from the device."""

    def __init__(self, hass: HomeAssistant, handler: AlsavoPro) -> None:
        """Initialize the coordinator."""
        self.data_handler = handler
        super().__init__(
            hass,
            _LOGGER,
            name="AlsavoPro",
            update_interval=timedelta(seconds=15),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from Alsavo Pro."""
        _LOGGER.debug("Updating Alsavo Pro data...")
        try:
            async with async_timeout.timeout(10):
                await self.data_handler.update()
                if not self.data_handler.data:
                    raise UpdateFailed("No data returned from Alsavo Pro")
                return self.data_handler.data
        except Exception as err:
            raise UpdateFailed(f"Error updating Alsavo Pro data: {err}") from err
