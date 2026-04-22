"""
Timezone Helper - Complete working version
Auto-detects local timezone via IP geolocation.
"""

from datetime import datetime
import zoneinfo
import httpx
import logging

logger = logging.getLogger(__name__)


def detect_timezone() -> zoneinfo.ZoneInfo:
    """
    Detect local timezone via IP geolocation.
    Falls back to Europe/Berlin.
    """
    apis = [
        ("https://ipapi.co/json/", lambda d: d.get("timezone")),
        ("https://ip-api.com/json/", lambda d: d.get("timezone")),
    ]
    
    for url, extractor in apis:
        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                tz_name = extractor(data)
                if tz_name:
                    logger.info(f"Timezone detected: {tz_name}")
                    return zoneinfo.ZoneInfo(tz_name)
        except Exception as e:
            logger.debug(f"Detection failed: {e}")
    
    logger.warning("Fallback to Europe/Berlin")
    return zoneinfo.ZoneInfo("Europe/Berlin")


# Detect once at import
LOCAL_TZ = detect_timezone()
UTC_TZ = zoneinfo.ZoneInfo("UTC")


def now_local() -> datetime:
    """Current time in local timezone."""
    return datetime.now(LOCAL_TZ)


def now_utc() -> datetime:
    """Current time in UTC."""
    return datetime.now(UTC_TZ)


def utc_to_local(utc_dt: datetime) -> datetime:
    """Convert UTC datetime to local timezone."""
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=UTC_TZ)
    return utc_dt.astimezone(LOCAL_TZ)