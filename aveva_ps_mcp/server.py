"""MCP Server definition with all AVEVA Process Simulation tools."""

import json
import logging
from mcp.server.fastmcp import FastMCP

from .config import load_config
from .automation.base import connect_to_aps, disconnect, get_aps_info
from .automation.simulation import (
    open_simulation,
    close_simulation,
    stop_solver,
    run_dynamics,
    run_steady_state,
    restore_snapshot,
    create_snapshot,
    list_snapshots,
    get_simulation_status,
)
from .automation.flowsheet import (
    list_unit_operations,
    list_streams,
    get_stream_properties,
    set_stream_property,
    get_stream_composition,
    get_unit_operation_properties,
    set_unit_operation_property,
)

config = load_config()
logging.basicConfig(level=getattr(logging, config.get("log_level", "INFO")))
logger = logging.getLogger("aveva_ps_mcp")

mcp = FastMCP(
    "aveva-process-simulation",
    description="MCP server to automate AVEVA Process Simulation using Claude AI",
)


# ── Connection Tools ──────────────────────────────────────────────────────────

@mcp.tool()
def connect_aps() -> str:
    """Connect to a running AVEVA Process Simulation instance via simcentralconnect."""
    return json.dumps(connect_to_aps(), indent=2)


@mcp.tool()
def disconnect_aps() -> str:
    """Disconnect from AVEVA Process Simulation."""
    return json.dumps(disconnect(), indent=2)


@mcp.tool()
def get_aps_environment() -> str:
    """Get information about the AVEVA Process Simulation environment and connection status."""
    return json.dumps(get_aps_info(), indent=2)


# ── Simulation Lifecycle Tools ────────────────────────────────────────────────

@mcp.tool()
def open_sim(simulation_name: str) -> str:
    """Open a simulation by its exact name in AVEVA Process Simulation.

    Args:
        simulation_name: The exact name of the simulation to open (e.g., "Sim 3")
    """
    return json.dumps(open_simulation(simulation_name), indent=2)


@mcp.tool()
def close_sim() -> str:
    """Close the currently open simulation."""
    return json.dumps(close_simulation(), indent=2)


@mcp.tool()
def stop_sim_solver() -> str:
    """Stop/pause the simulation solver."""
    return json.dumps(stop_solver(), indent=2)


@mcp.tool()
def run_dynamics_sim(duration: float) -> str:
    """Run the dynamic simulation for a specified duration.

    Args:
        duration: Duration in seconds to run the dynamics simulation
    """
    return json.dumps(run_dynamics(duration), indent=2)


@mcp.tool()
def run_steady_state_sim() -> str:
    """Run a steady-state simulation solve."""
    return json.dumps(run_steady_state(), indent=2)


@mcp.tool()
def get_sim_status() -> str:
    """Get the current simulation status (mode, time, solver state)."""
    return json.dumps(get_simulation_status(), indent=2)


# ── Snapshot Tools ────────────────────────────────────────────────────────────

@mcp.tool()
def save_snapshot(snapshot_name: str) -> str:
    """Save a snapshot of the current simulation state.

    Args:
        snapshot_name: Name to give the snapshot
    """
    return json.dumps(create_snapshot(snapshot_name), indent=2)


@mcp.tool()
def load_snapshot(snapshot_name: str) -> str:
    """Restore the simulation to a previously saved snapshot state.

    Args:
        snapshot_name: Name of the snapshot to restore
    """
    return json.dumps(restore_snapshot(snapshot_name), indent=2)


@mcp.tool()
def get_snapshots() -> str:
    """List all available snapshots in the current simulation."""
    return json.dumps(list_snapshots(), indent=2)


# ── Flowsheet Tools ──────────────────────────────────────────────────────────

@mcp.tool()
def get_unit_operations() -> str:
    """List all unit operations (equipment) in the current flowsheet."""
    return json.dumps(list_unit_operations(), indent=2)


@mcp.tool()
def get_streams() -> str:
    """List all streams in the current flowsheet."""
    return json.dumps(list_streams(), indent=2)


@mcp.tool()
def read_stream(stream_name: str) -> str:
    """Read the properties of a stream (temperature, pressure, flow, etc.).

    Args:
        stream_name: Name of the stream to read
    """
    return json.dumps(get_stream_properties(stream_name), indent=2)


@mcp.tool()
def write_stream(stream_name: str, property_name: str, value: float) -> str:
    """Set a property value on a stream.

    Args:
        stream_name: Name of the stream
        property_name: Property to set (e.g., Temperature, Pressure, MassFlow)
        value: Numeric value to assign
    """
    return json.dumps(set_stream_property(stream_name, property_name, value), indent=2)


@mcp.tool()
def read_stream_composition(stream_name: str) -> str:
    """Get the mole fraction composition of a stream.

    Args:
        stream_name: Name of the stream
    """
    return json.dumps(get_stream_composition(stream_name), indent=2)


@mcp.tool()
def read_unit_operation(unit_name: str) -> str:
    """Read the properties of a unit operation (equipment).

    Args:
        unit_name: Name of the unit operation
    """
    return json.dumps(get_unit_operation_properties(unit_name), indent=2)


@mcp.tool()
def write_unit_operation(unit_name: str, property_name: str, value: float) -> str:
    """Set a property value on a unit operation.

    Args:
        unit_name: Name of the unit operation
        property_name: Property to set (e.g., DutyIn, Efficiency, PressureDrop)
        value: Numeric value to assign
    """
    return json.dumps(set_unit_operation_property(unit_name, property_name, value), indent=2)


# ── Utility Tools ────────────────────────────────────────────────────────────

@mcp.tool()
def execute_script(code: str) -> str:
    """Execute a Python script in the AVEVA Process Simulation scripting context.
    The 'sc' variable (simcentralconnect connection) is available in the script.

    Args:
        code: Python code to execute. The connection object is available as 'sc'.
    """
    from .automation.base import get_connection
    sc = get_connection()
    if sc is None:
        return json.dumps({"success": False, "error": "Not connected to APS"})
    try:
        local_vars = {"sc": sc, "result": None}
        exec(code, {}, local_vars)
        output = local_vars.get("result", None)
        return json.dumps({
            "success": True,
            "result": str(output) if output is not None else "Script executed (no result variable set)"
        })
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
