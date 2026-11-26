"""Configuration management for AVEVA Process Simulation MCP Server."""

import json
import os
from pathlib import Path

DEFAULT_CONFIG = {
    "default_unit": "SI",
    "log_level": "INFO",
    "connection_timeout": 30,
    "dynamics_run_duration": 10.0,
    "snapshot_name": "",
    "udp": {
        "bind_ip": "127.0.0.1",
        "peer_ip": "127.0.0.1",
        "receive_port": 5005,
        "send_port": 5006,
        "command_format": "json"
    }
}


def load_config() -> dict:
    config_path = Path(__file__).parent / "config.json"
    config = DEFAULT_CONFIG.copy()
    if config_path.exists():
        with open(config_path, "r") as f:
            user_config = json.load(f)
        config.update(user_config)
    return config
