import asyncio
import os
import sys
import json
import re
from typing import Optional
from contextlib import AsyncExitStack
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import google.generativeai as genai

load_dotenv()  # load environment variables from .env


class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

        # Initialize Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.gemini = genai.GenerativeModel("gemini-2.0-flash")

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server"""
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(command=command, args=[server_script_path], env=None)

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using Gemini and available tools"""
        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        tool_descriptions = "\n".join([
            f"{tool['name']}: {tool['description']}" for tool in available_tools
        ])

        prompt = f"""You are a helpful AI assistant. The user may ask questions or request tools.

Available tools:
{tool_descriptions}

If a tool needs to be used, respond with:
Call tool TOOL_NAME with args JSON_ARGUMENTS

User query:
{query}
"""

        gemini_response = self.gemini.generate_content(prompt)
        text = gemini_response.text.strip()
        final_text = [text]

        match = re.search(r"Call tool (\w+) with args (.+)", text)
        if match:
            tool_name = match.group(1)
            args_str = match.group(2)

            try:
                tool_args = json.loads(args_str)
                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(f"[Tool {tool_name} executed]")
                final_text.append(f"Tool result:\n{result.content}")
            except Exception as e:
                final_text.append(f"[Failed to call tool: {str(e)}]")

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break
                response = await self.process_query(query)
                print("\n" + response)
            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
