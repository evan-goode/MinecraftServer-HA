"""
Sensor to check the status of a Minecraft server.

"""
import logging
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from datetime import timedelta

ATTR_PING = 'Ping'
ATTR_USERS = 'Users Online'
ATTR_MOTD = 'MOTD'
ATTR_VERSION = 'Version'
ATTR_ONLINE = 'Online Players'
ATTR_MAXPLAYERS = 'Max Players'
ICON = 'mdi:minecraft'
REQUIREMENTS = ['mcstatus==2.1']

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)
logger = logging.getLogger(__name__)

# pylint: disable=unused-argument


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Minecraft server platform."""
    from mcstatus import MinecraftServer as mcserver

    server = config.get('server')
    name = config.get('name')

    if server is None:
        logger.error('No server specified')
        return False
    elif name is None:
        logger.error('No name specified')
        return False

    add_devices([
        MCServerSensor(server, name, mcserver)
    ])


class MCServerSensor(Entity):
    """A class for the Minecraft server."""

    # pylint: disable=abstract-method
    def __init__(self, server, name, mcserver):
        """Initialize the sensor."""
        self._mcserver = mcserver
        self._server = server
        self._name = name
        self.update()

    @property
    def name(self):
        """Return the name of the server."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    # pylint: disable=no-member
    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Update device state."""

        try:
            status = self._mcserver.lookup(self._server).status()
        except Exception as err:
            logger.error("Error connecting to server, assuming offline.")
            logger.debug("Server response: %s", str(err))
            status = self._state = "Offline"
        else:
            query = self._mcserver.lookup(self._server).query()
            self._state = str(status.players.online)
            self._online = status.players.online
            self._max = status.players.max
            self._ping = status.latency
            self._users = query.players.names
            self._motd = query.motd
            self._version = query.software.version

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
                ATTR_PING: self._ping,
                ATTR_ONLINE: self._online,
                ATTR_USERS: self._users,
                ATTR_MAXPLAYERS: self._max,
                ATTR_MOTD: self._motd,
                ATTR_VERSION: self._version
        }

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON
