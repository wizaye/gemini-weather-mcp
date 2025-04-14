# MCP Client

A Python client for interacting with Model Control Protocol (MCP) servers, enabling tool use through AI assistants.

## Overview

MCP Client is a bridge between Google's Gemini AI model and MCP-compatible servers. It allows you to:

1. Connect to MCP servers (Python or JavaScript)
2. Query the Gemini AI model
3. Execute tools provided by the server based on AI recommendations
4. Maintain an interactive chat session

## Requirements

- Python 3.13+
- Dependencies:
  - google-generativeai (≥0.8.4)
  - mcp (≥1.6.0)
  - python-dotenv (≥1.1.0)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/wizaye/gemini-weather-mcp.git
cd gemini-weather-mcp/mcp-client
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

## Configuration

1. Create a `.env` file in the project root (you can copy from `.env.example`):
```bash
cp .env.example .env
```

2. Add your Gemini API key to the `.env` file:
```
GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
```

You can obtain a Gemini API key from [Google AI Studio](https://makersuite.google.com/).

## Usage

Run the client by providing the path to an MCP-compatible server script:

```bash
 python client.py path/to/server_script.py
```
Using uv
```bash
 uv run client.py path/to/server_script.py
```
The client supports both Python and JavaScript server scripts.

### Interactive Chat

Once connected, you can interact with the AI assistant through the command line:

1. Type your query and press Enter  
2. The client will process your query using Gemini  
3. If appropriate, Gemini will recommend using a tool from the server  
4. The client will execute the tool and display the results  
5. Type `quit` to exit the chat session

## How It Works

1. **Initialization**: The client loads environment variables and initializes the Gemini model.

2. **Server Connection**: The client connects to the specified MCP server script and retrieves available tools.

3. **Query Processing**:
   - User queries are sent to Gemini along with information about available tools
   - Gemini decides whether to use a tool or respond directly
   - If a tool is needed, the client extracts the tool name and arguments from Gemini's response
   - The client calls the tool on the server and returns the combined results

4. **Chat Loop**: The client maintains an interactive session until the user types `quit`.

## Development

### Project Structure

- `client.py`: Main client implementation  
- `.env.example`: Template for environment variables  
- `pyproject.toml`: Project dependencies and metadata

### Adding New Features

To extend the client:

1. Modify the `MCPClient` class in `client.py`  
2. Add new methods for additional functionality  
3. Update the prompt template in `process_query()` to improve tool selection

## Troubleshooting

- **API Key Issues**: Ensure your Gemini API key is correctly set in the `.env` file  
- **Server Connection Errors**: Verify the server script path and ensure it's MCP-compatible  
- **Tool Execution Failures**: Check the server logs for detailed error information