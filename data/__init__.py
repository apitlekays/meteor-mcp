"""Aggregates all Meteor.js API data modules into a searchable registry."""

from .meteor_core import METEOR_CORE
from .methods import METHODS
from .pubsub import PUBSUB
from .collections import COLLECTIONS
from .accounts import ACCOUNTS
from .connections import CONNECTIONS
from .check import CHECK
from .ejson import EJSON
from .tracker import TRACKER
from .session import SESSION
from .reactive_var import REACTIVE_VAR
from .reactive_dict import REACTIVE_DICT
from .email_pkg import EMAIL_PKG
from .assets import ASSETS
from .ddp_rate_limiter import DDP_RATE_LIMITER
from .webapp import WEBAPP
from .app_config import APP_CONFIG
from .package_js import PACKAGE_JS
from .timers import TIMERS
from .environment import ENVIRONMENT
from .examples import EXAMPLES  # noqa: F401 — dict of code examples, separate structure
from .guides import GUIDES  # noqa: F401 — dict of conceptual guides, separate structure

# API_REGISTRY contains only API entry dicts (list[dict]).
# EXAMPLES and GUIDES have different shapes (dict[str, dict]) and are
# consumed directly by tools.py via their own dedicated tool handlers.
API_REGISTRY: list[dict] = [
    *METEOR_CORE,
    *METHODS,
    *PUBSUB,
    *COLLECTIONS,
    *ACCOUNTS,
    *CONNECTIONS,
    *CHECK,
    *EJSON,
    *TRACKER,
    *SESSION,
    *REACTIVE_VAR,
    *REACTIVE_DICT,
    *EMAIL_PKG,
    *ASSETS,
    *DDP_RATE_LIMITER,
    *WEBAPP,
    *APP_CONFIG,
    *PACKAGE_JS,
    *TIMERS,
    *ENVIRONMENT,
]

MODULE_NAMES: set[str] = {entry["module"] for entry in API_REGISTRY}
