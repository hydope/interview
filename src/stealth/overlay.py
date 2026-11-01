# StealthInterview - Stealth Transparent Overlay
# Copyright (C) 2026 StealthInterview Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Transparent stealth overlay for rendering AI answers over video conferencing apps."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class OverlayConfig:
    """Configuration for the stealth overlay."""

    enabled: bool = True
    opacity: float = 0.85
    position: str = "top_right"  # top_right, top_left, bottom_right, bottom_left, center
    width: int = 400
    height: int = 300
    font_size: int = 14
    font_family: str = "Consolas"
    text_color: str = "#00FF00"
    background_color: str = "#000000"
    click_through: bool = True
    always_on_top: bool = True
    hide_from_taskbar: bool = True


class StealthOverlay:
    """
    Transparent overlay window that renders AI-generated answers
    over video conferencing applications without being captured
    by screen-sharing software.
    """

    def __init__(self, config: Optional[OverlayConfig] = None) -> None:
        """
        Initialize the stealth overlay.

        Args:
            config: Overlay configuration.
        """
        self.config = config or OverlayConfig()
        self._window = None
        self._is_visible = False
        self._current_text = ""

    def show(self) -> None:
        """Show the overlay window."""
        if not self.config.enabled:
            logger.info("Stealth overlay is disabled in configuration")
            return

        logger.info(
            "Showing stealth overlay at %s (%dx%d, opacity=%.2f)",
            self.config.position,
            self.config.width,
            self.config.height,
            self.config.opacity,
        )
        self._is_visible = True

    def hide(self) -> None:
        """Hide the overlay window."""
        logger.info("Hiding stealth overlay")
        self._is_visible = False

    def update_text(self, text: str) -> None:
        """
        Update the text displayed on the overlay.

        Args:
            text: New text to display.
        """
        self._current_text = text
        if self._is_visible:
            logger.debug("Overlay text updated: %s", text[:80])

    def clear(self) -> None:
        """Clear the overlay text."""
        self._current_text = ""
        if self._is_visible:
            logger.debug("Overlay text cleared")

    def is_visible(self) -> bool:
        """Return whether the overlay is currently visible."""
        return self._is_visible

    def toggle(self) -> None:
        """Toggle overlay visibility."""
        if self._is_visible:
            self.hide()
        else:
            self.show()