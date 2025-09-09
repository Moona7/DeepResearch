from mcp_use import MCPClient

async def init_mcp(config_path: str) -> MCPClient:
    client = MCPClient.from_config_file(config_path)
    await client.create_all_sessions()
    return client
