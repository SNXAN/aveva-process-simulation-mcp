"""Core connection management for AVEVA Process Simulation."""

import logging

logger = logging.getLogger("aveva_ps_mcp")

_connection = None
_simulation_name = None


def connect_to_aps():
    """Connect to AVEVA Process Simulation via simcentralconnect."""
    global _connection
    try:
        import simcentralconnect
        _connection = simcentralconnect.connect()
        if _connection is None:
            return {"success": False, "error": "simcentralconnect.connect() returned None"}
        result = _connection.Result
        logger.info("Connected to AVEVA Process Simulation")
        return {
            "success": True,
            "message": "Connected to AVEVA Process Simulation",
            "result": str(result) if result else "OK"
        }
    except ImportError:
        return {
            "success": False,
            "error": (
                "simcentralconnect module not found. "
                "Ensure you are running Python from the AVEVA Process Simulation environment "
                "where the Scripting Interface SDK is installed."
            )
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_connection():
    """Return the current connection object, or None."""
    return _connection


def is_connected() -> bool:
    return _connection is not None


def disconnect():
    """Disconnect from AVEVA Process Simulation."""
    global _connection, _simulation_name
    try:
        if _connection is not None:
            _connection = None
            _simulation_name = None
            return {"success": True, "message": "Disconnected from AVEVA Process Simulation"}
        return {"success": True, "message": "No active connection"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_aps_info():
    """Get information about the AVEVA Process Simulation environment."""
    try:
        import simcentralconnect
        info = {
            "module": "simcentralconnect",
            "module_path": getattr(simcentralconnect, "__file__", "unknown"),
            "connected": is_connected(),
        }
        if is_connected():
            info["simulation"] = _simulation_name or "unknown"
        return {"success": True, "info": info}
    except ImportError:
        return {
            "success": False,
            "error": "simcentralconnect module not found"
        }
