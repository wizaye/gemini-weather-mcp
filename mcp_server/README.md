# MCP Server

A Python server implementing the Model Control Protocol (MCP) to provide weather-related tools for AI assistants.

## Overview

MCP Server is a FastMCP implementation that provides weather data tools through the National Weather Service API. It allows AI assistants to:

1. Retrieve weather alerts for US states
2. Get detailed weather forecasts for specific locations
3. Access formatted weather data through a standardized interface

## Requirements

- Python 3.13+
- Dependencies:
  - httpx (≥0.28.1)
  - mcp[cli] (≥1.6.0)

## Installation

1. Clone this repository:
```bash
git clone <REPO_URL>
cd mcp-server
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Option A: Install dependencies using `pip` (standard)

```bash
pip install -e .
```

### Option B: Install dependencies using `uv` (faster and more secure)

> 💡 [`uv`](https://github.com/astral-sh/uv) is a modern Python package manager with improved speed and dependency resolution.  
> To install `uv`:
```bash
pip install uv  # or follow other install methods at https://github.com/astral-sh/uv
```

Then install dependencies:
```bash
uv pip install -e .
```

## Usage

Run the weather server:

```bash
python weather.py
```

Using uv:
```bash
uv run weather.py
```

The server will start in stdio mode, which allows it to communicate with MCP clients.

### Available Tools

The server provides the following tools:

#### 1. Get Weather Alerts

Retrieves active weather alerts for a US state.

**Input:**
- `state`: Two-letter US state code (e.g., CA, NY)

**Output:**
- Formatted list of active weather alerts including event type, area, severity, description, and instructions

#### 2. Get Weather Forecast

Retrieves a detailed weather forecast for a specific location.

**Input:**
- `latitude`: Latitude of the location
- `longitude`: Longitude of the location

**Output:**
- Detailed forecast for the next 5 periods, including temperature, wind conditions, and forecast details

## How It Works

1. **Initialization**: The server initializes a FastMCP instance with the name "weather".

2. **API Integration**: The server communicates with the National Weather Service API to fetch weather data.

3. **Tool Implementation**: 
   - Each tool is implemented as an async function decorated with `@mcp.tool()`
   - Tools handle input validation, API requests, and formatting of responses
   - Error handling ensures graceful degradation when API requests fail

4. **Transport**: The server uses stdio transport for communication with MCP clients.

## Development

### Project Structure

- `weather.py`: Main server implementation with tool definitions
- `pyproject.toml`: Project dependencies and metadata

### Adding New Tools

To add a new weather-related tool:

1. Create a new async function in `weather.py`
2. Decorate it with `@mcp.tool()`
3. Implement the tool logic, including API requests and response formatting
4. Ensure proper error handling

### API Usage Notes

- The server uses the National Weather Service API (api.weather.gov)
- A custom User-Agent is set to identify the application
- Requests include proper headers for JSON responses
- Error handling is implemented to gracefully handle API failures

## Troubleshooting

- **API Connection Issues**: Ensure you have internet connectivity and the NWS API is available
- **Tool Execution Failures**: Check for proper input formatting and valid geographic coordinates
- **Client Connection Problems**: Verify that the client is properly configured to connect to the server
