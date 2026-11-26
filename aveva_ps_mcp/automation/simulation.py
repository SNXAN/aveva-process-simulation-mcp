"""Simulation lifecycle management for AVEVA Process Simulation."""

import logging
from .base import get_connection, is_connected

logger = logging.getLogger("aveva_ps_mcp")


def _require_connection():
    if not is_connected():
        return {"success": False, "error": "Not connected to APS. Call connect_aps first."}
    return None


def open_simulation(simulation_name: str):
    """Open a simulation by name in AVEVA Process Simulation."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        result = sc.OpenSimulation(simulation_name).Result
        from .base import _simulation_name
        import aveva_ps_mcp.automation.base as base_mod
        base_mod._simulation_name = simulation_name
        logger.info(f"Opened simulation: {simulation_name}")
        return {
            "success": True,
            "message": f"Opened simulation '{simulation_name}'",
            "result": str(result) if result else "OK"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def close_simulation():
    """Close the current simulation."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        sc.CloseSimulation()
        import aveva_ps_mcp.automation.base as base_mod
        base_mod._simulation_name = None
        return {"success": True, "message": "Simulation closed"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def stop_solver():
    """Stop the solver / pause the simulation."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        sc.StopSolver()
        return {"success": True, "message": "Solver stopped"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_dynamics(duration: float):
    """Run the dynamic simulation for a specified duration (seconds)."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        result = sc.RunDynamics(duration)
        success = bool(result) if result is not None else True
        return {
            "success": success,
            "message": f"RunDynamics({duration}s) completed",
            "result": str(result) if result else "OK"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_steady_state():
    """Run a steady-state simulation solve."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        result = sc.RunSteadyState()
        return {
            "success": True,
            "message": "Steady-state solve completed",
            "result": str(result) if result else "OK"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def restore_snapshot(snapshot_name: str):
    """Restore a named snapshot (returns simulation to a saved state)."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        sc.StopSolver()
        sc.RestoreSnapshot(snapshot_name)
        return {
            "success": True,
            "message": f"Snapshot '{snapshot_name}' restored"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def create_snapshot(snapshot_name: str):
    """Create/save a named snapshot of the current simulation state."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        sc.CreateSnapshot(snapshot_name)
        return {
            "success": True,
            "message": f"Snapshot '{snapshot_name}' created"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_snapshots():
    """List available snapshots in the current simulation."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        snapshots = sc.GetSnapshots()
        snapshot_list = list(snapshots) if snapshots else []
        return {
            "success": True,
            "snapshots": snapshot_list,
            "count": len(snapshot_list)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_simulation_status():
    """Get the current simulation status (mode, time, solver state)."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        status = {}
        for attr in ["SimulationTime", "Mode", "SolverStatus", "SimulationName"]:
            try:
                status[attr] = str(getattr(sc, attr, "N/A"))
            except Exception:
                status[attr] = "N/A"
        return {"success": True, "status": status}
    except Exception as e:
        return {"success": False, "error": str(e)}
