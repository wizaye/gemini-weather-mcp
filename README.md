# Gemini Weather MCP: Model Control Protocol Implementation Using Python and GEMINI API

This repository contains a complete implementation of the Model Control Protocol (MCP), enabling AI assistants to access external tools and data sources. The project consists of two main components:

1. **MCP Client**: A Python client that connects AI models (Gemini) to MCP-compatible servers
2. **MCP Server**: A Python server that provides weather data tools through the National Weather Service API

## Project Structure

```
gemini-weather-mcp/
├── mcp_client/         # Client implementation for connecting to MCP servers
└── mcp_server/         # Server implementation providing weather data tools
```

## MCP Client

The MCP Client serves as a bridge between Google's Gemini AI model and MCP-compatible servers. It allows you to:

1. Connect to MCP servers (Python or JavaScript)
2. Query the Gemini AI model
3. Execute tools provided by the server based on AI recommendations
4. Maintain an interactive chat session

### Requirements

- Python 3.13+
- Dependencies:
  - google-generativeai (≥0.8.4)
  - mcp (≥1.6.0)
  - python-dotenv (≥1.1.0)

### Usage

Run the client by providing the path to an MCP-compatible server script:

```bash
python mcp_client/client.py mcp_server/weather.py
```

Using uv:
```bash
uv run mcp_client/client.py mcp_server/weather.py
```

## MCP Server

The MCP Server is a FastMCP implementation that provides weather data tools through the National Weather Service API. It allows AI assistants to:

1. Retrieve weather alerts for US states
2. Get detailed weather forecasts for specific locations
3. Access formatted weather data through a standardized interface

### Requirements

- Python 3.13+
- Dependencies:
  - httpx (≥0.28.1)
  - mcp[cli] (≥1.6.0)

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

## Installation

1. Clone this repository:
```bash
git clone https://github.com/wizaye/gemini-weather-mcp.git
cd gemini-weather-mcp
```

2. Set up the client:
```bash
cd mcp_client
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

3. Create a `.env` file with your Gemini API key:
```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

4. Set up the server:
```bash
cd ../mcp_server
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## How It Works

1. **Client Initialization**: The client loads the Gemini API key and initializes the model.

2. **Server Connection**: The client connects to the MCP server using stdio transport.

3. **Tool Discovery**: The client queries the server for available tools.

4. **Query Processing**: 
   - User queries are sent to the Gemini model along with tool descriptions
   - Gemini decides whether to use tools based on the query
   - If a tool is needed, the client executes it through the MCP server
   - Results are returned to the user

5. **Weather Data**: The server fetches real-time weather data from the National Weather Service API.

## Troubleshooting

### Client Issues
- **API Key Issues**: Ensure your Gemini API key is correctly set in the `.env` file
- **Server Connection Errors**: Verify the server script path and ensure it's MCP-compatible
- **Tool Execution Failures**: Check the server logs for detailed error information

### Server Issues
- **API Connection Issues**: Ensure you have internet connectivity and the NWS API is available
- **Tool Execution Failures**: Check for proper input formatting and valid geographic coordinates
- **Client Connection Problems**: Verify that the client is properly configured to connect to the server

## Development

To add new tools to the server:

1. Create a new async function in `weather.py`
2. Decorate it with `@mcp.tool()`
3. Implement the tool logic, including API requests and response formatting
4. Ensure proper error handling

To modify the client behavior:

1. Update the prompt template in `process_query()` to change how Gemini interprets user queries
2. Modify the tool execution logic to handle different response formats
