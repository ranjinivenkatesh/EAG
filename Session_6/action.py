from utils import parse_function_call_params, validate_against_schema

async def perform_action(session, tools, func_name, param_parts):
    tool = next((t for t in tools if t.name == func_name), None)
    print("in perform_action")
    print(tool)
    if not tool:
        print(f"⚠️ Tool {func_name} not found. Skipping this iteration.")
        return f"Tool {func_name} not available."

    args = parse_function_call_params(param_parts)
    try:
        args = validate_against_schema(tool, args)
    except Exception as e:
        return f"Validation error before tool call: {e}"

    try:
        result = await session.call_tool(func_name, arguments=args)
        if hasattr(result, 'content'):
            if isinstance(result.content, list):
                return [item.text for item in result.content]
            return result.content
        return str(result)
    except Exception as e:
        return f"Tool execution error: {e}"
