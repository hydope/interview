# StealthInterview - Configuration Loader
# Copyright (C) 2026 StealthInterview Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""YAML configuration loader with environment variable support."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path("config/config.yaml")
EXAMPLE_CONFIG_PATH = Path("examples/config.example.yaml")


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """
    Load configuration from YAML file with environment variable overrides.

    Args:
        config_path: Path to config YAML. Defaults to config/config.yaml.

    Returns:
        Configuration dictionary.

    Raises:
        FileNotFoundError: If config file does not exist.
    """
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH

    if not path.exists():
        logger.warning("Config file not found: %s", path)
        if EXAMPLE_CONFIG_PATH.exists():
            logger.info("Loading example config from: %s", EXAMPLE_CONFIG_PATH)
            path = EXAMPLE_CONFIG_PATH
        else:
            logger.error("No config file found. Using defaults.")
            return {}

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    # Apply environment variable overrides (STT__MODEL, LLM__TEMPERATURE, etc.)
    config = _apply_env_overrides(config)

    logger.info("Configuration loaded from %s", path)
    return config


def _apply_env_overrides(config: dict[str, Any]) -> dict[str, Any]:
    """
    Apply environment variable overrides to config.

    Environment variables use double underscore as separator:
    STT__MODEL=large -> config["stt"]["model"] = "large"
    """
    for key, value in os.environ.items():
        if "__" in key:
            parts = key.lower().split("__")
            current = config
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            # Try to convert value to appropriate type
            current[parts[-1]] = _coerce_value(value)

    return config


def _coerce_value(value: str) -> Any:
    """Coerce a string environment variable to int/float/bool if possible."""
    # Boolean
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    # Integer
    try:
        return int(value)
    except ValueError:
        pass
    # Float
    try:
        return float(value)
    except ValueError:
        pass
    return value