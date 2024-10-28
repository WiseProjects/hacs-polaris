from itertools import cycle, islice
from typing import Final


from dataclasses import dataclass
from homeassistant.components.switch import SwitchDeviceClass, SwitchEntityDescription
from homeassistant.helpers.entity import EntityCategory


DOMAIN: Final = "polaris"

ATTR_NAME = "name"
ATTR_ERROR = "error"
ATTR_STATE = "state"

CONF_TOPIC_PREFIX = "topic_prefix"
MQTT_DEVICE_FOUND = "device_found"

POLARIS_DEVICE = {
    34: {"model": "PHB-1551WIFI", "class": "Blender"},
    93: {"model": "PHB-1350WIFI", "class": "Blender"},
    11: {"model": "PWH-IDF06", "class": "Boiler"},
    30: {"model": "SIGMA WI-FI", "class": "Boiler"},
    31: {"model": "ENIGMA WI-FI", "class": "Boiler"},
    7: {"model": "PVCR-3200", "class": "Cleaner"},
    12: {"model": "PVCR-3300", "class": "Cleaner"},
    19: {"model": "PVCR-0833", "class": "Cleaner"},
    21: {"model": "PVCR-0735", "class": "Cleaner"},
    22: {"model": "PVCR-1050", "class": "Cleaner"},
    23: {"model": "PVCR-1028", "class": "Cleaner"},
    24: {"model": "PVCR-1229", "class": "Cleaner"},
    43: {"model": "PVCR-0833", "class": "Cleaner"},
    66: {"model": "PVCR-3900", "class": "Cleaner"},
    68: {"model": "PVCR-3100", "class": "Cleaner"},
    76: {"model": "PVCR-3200", "class": "Cleaner"},
    81: {"model": "PVCR-3400", "class": "Cleaner"},
    88: {"model": "PVCR-3800", "class": "Cleaner"},
    90: {"model": "PVCS-2090", "class": "Cleaner"},
    100: {"model": "PVCR Wave-15", "class": "Cleaner"},
    101: {"model": "PVCR-0726 Aqua", "class": "Cleaner"},
    102: {"model": "PVCR-1226 Aqua", "class": "Cleaner"},
    104: {"model": "PVCR-0905", "class": "Cleaner"},
    107: {"model": "PVCR-0926", "class": "Cleaner"},
    108: {"model": "PVCR-0726 GYRO", "class": "Cleaner"},
    109: {"model": "PVCR-1226 GYRO", "class": "Cleaner"},
    110: {"model": "PVCR-4105", "class": "Cleaner"},
    111: {"model": "PVCS-1150", "class": "Cleaner"},
    112: {"model": "PVCR-3700", "class": "Cleaner"},
    113: {"model": "PVCR-4000", "class": "Cleaner"},
    115: {"model": "PVCR-3200", "class": "Cleaner"},
    119: {"model": "PVCR-5001", "class": "Cleaner"},
    123: {"model": "PVCR-6001", "class": "Cleaner"},
    124: {"model": "PVCRDC-5002", "class": "Cleaner"},
    125: {"model": "PVCRDC-6002", "class": "Cleaner"},
    45: {"model": "PCM-1540WIFI", "class": "Coffeemaker"},
    103: {"model": "PACM-2080AC", "class": "Coffeemaker"},
    1: {"model": "EVO-0225", "class": "Cooker"},
    9: {"model": "PMC-0526WIFI", "class": "Cooker"},
    10: {"model": "PMC-0521WIFI", "class": "Cooker"},
    32: {"model": "PMC-0524WIFI", "class": "Cooker"},
    33: {"model": "PMC-0530WIFI", "class": "Cooker"},
    39: {"model": "PMC-0528WIFI", "class": "Cooker"},
    40: {"model": "PMC-0526WIFI", "class": "Cooker"},
    41: {"model": "PMC-0521WIFI", "class": "Cooker"},
    47: {"model": "PMC-0530WIFI", "class": "Cooker"},
    48: {"model": "PMC-0528WIFI", "class": "Cooker"},
    55: {"model": "PMC-0524WIFI", "class": "Cooker"},
    77: {"model": "PMC-5040WIFI", "class": "Cooker"},
    78: {"model": "PMC-5050WIFI", "class": "Cooker"},
    79: {"model": "PMC-5017WIFI", "class": "Cooker"},
    80: {"model": "PMC-5020WIFI", "class": "Cooker"},
    89: {"model": "PMC-5055WIFI", "class": "Cooker"},
    95: {"model": "PMC-00000", "class": "Cooker"},
    114: {"model": "PMC-0526WIFI-G", "class": "Cooker"},
    3: {"model": "PWS1886/1892", "class": "Floor-scales"},
    5: {"model": "PWS1830/1883", "class": "Floor-scales"},
    96: {"model": "PGP-4001", "class": "Grill"},
    122: {"model": "PGP-4001-DEV", "class": "Grill"},
    16: {"model": "PHV-1401", "class": "Heater"},
    46: {"model": "PCH-0320WIFI", "class": "Heater"},
    49: {"model": "PMH-21XX", "class": "Heater"},
    64: {"model": "PMH-21XX", "class": "Heater"},
    65: {"model": "PCH-0320WIFI", "class": "Heater"},
    4: {"model": "PUH-9105", "class": "Humidifier"},
    15: {"model": "PUH-7406", "class": "Humidifier"},
    17: {"model": "PUH-9105", "class": "Humidifier"},
    18: {"model": "PUH-9105", "class": "Humidifier"},
    25: {"model": "PUH-6090", "class": "Humidifier"},
    44: {"model": "PUH-9105", "class": "Humidifier"},
    70: {"model": "PUH-9105", "class": "Humidifier"},
    71: {"model": "PUH-1010", "class": "Humidifier"},
    72: {"model": "PUH-2300", "class": "Humidifier"},
    73: {"model": "PUH-3030", "class": "Humidifier"},
    74: {"model": "PUH-9009", "class": "Humidifier"},
    75: {"model": "PUH-4040", "class": "Humidifier"},
    87: {"model": "PUH-8080", "class": "Humidifier"},
    99: {"model": "PUH-4040", "class": "Humidifier"},
    91: {"model": "PIR-2624AK 3m", "class": "Iron"},
    2: {"model": "PWK 1775CGLD", "class": "Kettle"},
    6: {"model": "PWK 1725CGLD", "class": "Kettle"},
    8: {"model": "PWK 1755CAD", "class": "Kettle"},
    29: {"model": "PWK-1712CGLD", "class": "Kettle"},
    35: {"model": "PWK 1775CGLD", "class": "Kettle"},
    36: {"model": "PWK 1725CGLD", "class": "Kettle"},
    37: {"model": "PWK 1755CAD", "class": "Kettle"},
    38: {"model": "PWK-1712CGLD", "class": "Kettle"},
    51: {"model": "PWK 1775CGLD", "class": "Kettle"},
    52: {"model": "PWK 1725CGLD", "class": "Kettle"},
    53: {"model": "PWK 1755CAD", "class": "Kettle"},
    54: {"model": "PWK-1712CGLD", "class": "Kettle"},
    56: {"model": "PWK 1775CGLD", "class": "Kettle"},
    57: {"model": "PWK 1725CGLD", "class": "Kettle"},
    58: {"model": "PWK 1755CAD", "class": "Kettle"},
    59: {"model": "PWK-1712CGLD", "class": "Kettle"},
    60: {"model": "PWK 1775CGLD", "class": "Kettle"},
    61: {"model": "PWK 1725CGLD", "class": "Kettle"},
    62: {"model": "PWK 1755CAD", "class": "Kettle"},
    63: {"model": "PWK-1712CGLD", "class": "Kettle"},
    67: {"model": "PWK-1720CGLD", "class": "Kettle"},
    82: {"model": "PWK 1725CGLD", "class": "Kettle"},
    83: {"model": "PWK-1712CGLD RGB", "class": "Kettle"},
    84: {"model": "PWK-1720CGLD RGB", "class": "Kettle"},
    85: {"model": "PWK 1775CGLD SMART", "class": "Kettle"},
    86: {"model": "PWK 1725CGLD", "class": "Kettle"},
    97: {"model": "PWK-1712CGLD", "class": "Kettle"},
    98: {"model": "PWK 1775CGLD SCALES", "class": "Kettle"},
    105: {"model": "PWK 1725CGLD", "class": "Kettle"},
    106: {"model": "PWK 1725CGLD SCALES", "class": "Kettle"},
    116: {"model": "Smart-Lid", "class": "Kettle"},
    117: {"model": "PWK-1712CGLD", "class": "Kettle"},
    120: {"model": "HAIR-DRYER", "class": "Kettle"},
    92: {"model": "PGS-1450CWIFI", "class": "Steamer"},
    94: {"model": "PSS-7070KWIFI", "class": "Steamer"},
    26: {"model": "PTB-RMST201811", "class": "Toothbrush"},
    27: {"model": "PTB-RMST201908", "class": "Toothbrush"},
    28: {"model": "PTB-RMST201906", "class": "Toothbrush"},
    50: {"model": "PETB-0202TC", "class": "Toothbrush"},
}


@dataclass
class openwbSwitchEntityDescription(SwitchEntityDescription):
    """Enhance the select entity description for openWB."""

    mqttTopicCommand: str | None = None
    mqttTopicCurrentValue: str | None = None
    mqttTopicChargeMode: str | None = None


SWITCHES_PER_LP = [
    openwbSwitchEntityDescription(
        key="ChargePointEnabled",
        entity_category=EntityCategory.CONFIG,
        name="Включить",
        mqttTopicCommand="control/mode",
        mqttTopicCurrentValue="state/mode",
        device_class=SwitchDeviceClass.SWITCH,
    ),
    openwbSwitchEntityDescription(
        key="PriceBasedCharging",
        entity_category=EntityCategory.CONFIG,
        name="Без звука",
        device_class=SwitchDeviceClass.SWITCH,
        mqttTopicCommand="control/sound",
        mqttTopicCurrentValue="state/sound",
    ),
]
