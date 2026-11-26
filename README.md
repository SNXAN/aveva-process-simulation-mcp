# AVEVA Process Simulation MCP Server

Automate AVEVA Process Simulation (APS) using natural language through Claude AI and the Model Context Protocol (MCP).

## What is This?

An MCP server that lets Claude AI control AVEVA Process Simulation through natural language. Instead of manually clicking through the simulator GUI, you tell Claude what to do — and it drives the simulation for you.

**Example prompts:**
- "Connect to APS and open simulation 'Sim 3'"
- "Show me all the streams in the flowsheet"
- "Read the temperature and pressure of stream Feed-1"
- "Set the feed flow rate to 100 kg/s and run a steady-state solve"
- "Save a snapshot called 'baseline' and then run dynamics for 60 seconds"
- "List all unit operations and their properties"

## Available Tools (20 Tools)

| Category | Tool | Description |
|----------|------|-------------|
| Connection | `connect_aps` | Connect to running APS instance |
| Connection | `disconnect_aps` | Disconnect from APS |
| Connection | `get_aps_environment` | Get environment and connection info |
| Simulation | `open_sim` | Open a simulation by name |
| Simulation | `close_sim` | Close the current simulation |
| Simulation | `stop_sim_solver` | Stop/pause the solver |
| Simulation | `run_dynamics_sim` | Run dynamic simulation for a duration |
| Simulation | `run_steady_state_sim` | Run a steady-state solve |
| Simulation | `get_sim_status` | Get simulation mode, time, solver state |
| Snapshots | `save_snapshot` | Save current state as a named snapshot |
| Snapshots | `load_snapshot` | Restore a previously saved snapshot |
| Snapshots | `get_snapshots` | List all available snapshots |
| Flowsheet | `get_unit_operations` | List all equipment in the flowsheet |
| Flowsheet | `get_streams` | List all streams |
| Flowsheet | `read_stream` | Read stream properties (T, P, flow, etc.) |
| Flowsheet | `write_stream` | Set a stream property value |
| Flowsheet | `read_stream_composition` | Get mole fraction composition |
| Flowsheet | `read_unit_operation` | Read equipment properties |
| Flowsheet | `write_unit_operation` | Set an equipment property value |
| Utility | `execute_script` | Execute Python in the APS scripting context |

## Requirements

- **OS:** Windows 10 or Windows 11
- **AVEVA Process Simulation:** 2023 or later (installed and licensed)
- **Python:** 3.8+ (the environment where `import simcentralconnect` works)
- **Claude:** Claude Desktop app or Claude Code

## Quick Start

### 1. Clone the Repository
```
git clone https://github.com/YOUR_USERNAME/aveva-process-simulation-mcp.git
cd aveva-process-simulation-mcp
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Configure Claude

**For Claude Code**, add to your MCP settings:
```json
{
  "mcpServers": {
    "aveva-ps": {
      "command": "python",
      "args": ["C:\\path\\to\\aveva-process-simulation-mcp\\aveva_ps_mcp_server.py"]
    }
  }
}
```

**For Claude Desktop**, add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "aveva-ps": {
      "command": "python",
      "args": ["C:\\path\\to\\aveva-process-simulation-mcp\\aveva_ps_mcp_server.py"]
    }
  }
}
```

### 4. Launch
1. Open AVEVA Process Simulation first
2. Restart Claude Desktop / Claude Code
3. In Claude, type: "Connect to APS"
4. Start simulating!

## How It Works

```
┌──────────────────────┐                         ┌──────────────────────────┐
│     Claude AI        │    MCP Protocol          │  AVEVA Process Sim       │
│                      │◄───────────────────────►│                          │
│  Natural language    │    JSON-RPC over stdio   │  simcentralconnect API   │
│  commands            │                          │  ────────────────────    │
│                      │                          │  Flowsheet Model         │
│  "Read stream        │                          │  Streams & Equipment     │
│   Feed-1 temp"       │                          │  Dynamics Solver         │
│                      │                          │  Snapshot Manager        │
└──────────────────────┘                         └──────────────────────────┘
```

The MCP server uses `simcentralconnect` — the official AVEVA scripting API — to control the simulation lifecycle (open, run, stop, snapshot) and read/write process data.

## Configuration

Edit `aveva_ps_mcp/config.json`:

```json
{
  "default_unit": "SI",
  "log_level": "INFO",
  "connection_timeout": 30,
  "dynamics_run_duration": 10.0
}
```

## Project Structure

```
aveva-process-simulation-mcp/
├── aveva_ps_mcp_server.py          # Entry point
├── aveva_ps_mcp/                   # Main package
│   ├── __init__.py                # Package info (v1.0.0)
│   ├── server.py                  # MCP server & tool definitions
│   ├── config.py                  # Configuration management
│   ├── config.json                # Default settings
│   ├── automation/                # Core automation modules
│   │   ├── base.py               # Connection management
│   │   ├── simulation.py         # Simulation lifecycle
│   │   └── flowsheet.py          # Flowsheet, streams & equipment
│   └── utils/                    # Utility modules
├── requirements.txt
├── .gitignore
└── README.md
```

## Important Notes

- You must run Python from the AVEVA environment where `simcentralconnect` is available
- AVEVA Process Simulation must be running before connecting
- The `execute_script` tool runs arbitrary Python in the APS context — review before enabling in production
- API method names (GetStreams, RunDynamics, etc.) may vary by APS version — check your installation's Scripting Interface SDK docs

## Acknowledgements

- [AVEVA](https://www.aveva.com/) for AVEVA Process Simulation and the simcentralconnect API
- [SolidWorks MCP](https://github.com/alisamsam/solidworks-mcp) by Samsaam Ali Baig — architecture inspiration
- [AVEVA-Process-Simulation-UDP-SimcentralPython](https://github.com/VzequyU/AVEVA-Process-Simulation-UDP-SimcentralPython) by Ezequiel Valencia — API reference

## License

MIT License
