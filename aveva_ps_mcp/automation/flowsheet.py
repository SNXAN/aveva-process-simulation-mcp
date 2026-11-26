"""Flowsheet, stream, and unit operation tools for AVEVA Process Simulation."""

import logging
from .base import get_connection, is_connected

logger = logging.getLogger("aveva_ps_mcp")


def _require_connection():
    if not is_connected():
        return {"success": False, "error": "Not connected to APS. Call connect_aps first."}
    return None


def list_unit_operations():
    """List all unit operations in the current flowsheet."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        ops = sc.GetUnitOperations()
        op_list = []
        if ops:
            for op in ops:
                op_info = {"name": str(op)}
                try:
                    op_info["type"] = str(op.TypeName) if hasattr(op, "TypeName") else "unknown"
                except Exception:
                    pass
                op_list.append(op_info)
        return {"success": True, "unit_operations": op_list, "count": len(op_list)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_streams():
    """List all streams in the current flowsheet."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        streams = sc.GetStreams()
        stream_list = []
        if streams:
            for s in streams:
                s_info = {"name": str(s)}
                try:
                    s_info["type"] = str(s.TypeName) if hasattr(s, "TypeName") else "unknown"
                except Exception:
                    pass
                stream_list.append(s_info)
        return {"success": True, "streams": stream_list, "count": len(stream_list)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_stream_properties(stream_name: str):
    """Get properties of a specific stream (temperature, pressure, flow, composition)."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        stream = sc.GetStream(stream_name)
        if stream is None:
            return {"success": False, "error": f"Stream '{stream_name}' not found"}

        props = {}
        property_names = [
            "Temperature", "Pressure", "MassFlow", "MolarFlow",
            "VolumeFlow", "Enthalpy", "Entropy", "VaporFraction",
            "MolecularWeight", "Density"
        ]
        for prop in property_names:
            try:
                val = getattr(stream, prop, None)
                if val is not None:
                    props[prop] = float(val) if not isinstance(val, str) else val
            except Exception:
                pass

        return {"success": True, "stream": stream_name, "properties": props}
    except Exception as e:
        return {"success": False, "error": str(e)}


def set_stream_property(stream_name: str, property_name: str, value: float):
    """Set a property value on a stream."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        stream = sc.GetStream(stream_name)
        if stream is None:
            return {"success": False, "error": f"Stream '{stream_name}' not found"}

        setattr(stream, property_name, value)
        return {
            "success": True,
            "message": f"Set {stream_name}.{property_name} = {value}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_stream_composition(stream_name: str):
    """Get the composition (mole fractions) of a stream."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        stream = sc.GetStream(stream_name)
        if stream is None:
            return {"success": False, "error": f"Stream '{stream_name}' not found"}

        composition = {}
        try:
            comp = stream.GetComposition()
            if comp:
                for component in comp:
                    composition[str(component.Name)] = float(component.MoleFraction)
        except Exception:
            try:
                comp = stream.Composition
                if comp:
                    composition = {str(k): float(v) for k, v in comp.items()}
            except Exception:
                pass

        return {"success": True, "stream": stream_name, "composition": composition}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_unit_operation_properties(unit_name: str):
    """Get properties of a specific unit operation."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        unit = sc.GetUnitOperation(unit_name)
        if unit is None:
            return {"success": False, "error": f"Unit operation '{unit_name}' not found"}

        props = {}
        common_props = [
            "Name", "TypeName", "DutyIn", "DutyOut",
            "InletTemperature", "OutletTemperature",
            "InletPressure", "OutletPressure",
            "PressureDrop", "Efficiency"
        ]
        for prop in common_props:
            try:
                val = getattr(unit, prop, None)
                if val is not None:
                    props[prop] = float(val) if isinstance(val, (int, float)) else str(val)
            except Exception:
                pass

        return {"success": True, "unit_operation": unit_name, "properties": props}
    except Exception as e:
        return {"success": False, "error": str(e)}


def set_unit_operation_property(unit_name: str, property_name: str, value: float):
    """Set a property value on a unit operation."""
    err = _require_connection()
    if err:
        return err
    try:
        sc = get_connection()
        unit = sc.GetUnitOperation(unit_name)
        if unit is None:
            return {"success": False, "error": f"Unit operation '{unit_name}' not found"}

        setattr(unit, property_name, value)
        return {
            "success": True,
            "message": f"Set {unit_name}.{property_name} = {value}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
