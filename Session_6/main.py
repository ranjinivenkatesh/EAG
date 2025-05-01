import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from perception import get_initial_prompt, get_llm_response
from decision import interpret_response
from action import perform_action
from memory import get_memory_log, reset_memory, update_memory
max_iterations = 25
async def main():
    reset_memory()

    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server_assignment5.py"]
        
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools

            user_query = """Complete each step in sequence, validating before proceeding to the next:
                1. Convert each character in "INDIA" to its ASCII value
                2. Calculate the exponential of each ASCII value and find their sum which is the final answer
                3. Start the paint application
                4. After paint is confirmed open, create a rectangle in the center
                5. After rectangle is confirmed drawn, place the calculated sum inside it
                6. Validation of inputs and outputs is a must """
            tool_descriptions = [f"{t.name} - {getattr(t, 'description', '')}" for t in tools]
            print(tool_descriptions)
            system_prompt = get_initial_prompt(tool_descriptions)

            iteration = 0

            while iteration < max_iterations:
                print("iteration",iteration)
                prompt = system_prompt + "\n\nQuery: " + user_query
                log = get_memory_log()
                if log:
                    print("memory logs is",log)
                    prompt += "\n\n" + "\n".join(log)

                llm_reply = await get_llm_response(prompt)
                action_type, content = interpret_response(llm_reply)

                if action_type == "FUNCTION_CALL":
                    print("action type is functiona call")
                    func_name, param_parts = content
                    print(func_name)
                    result = await perform_action(session, tools, func_name, param_parts)
                    update_memory(f"Called {func_name} with {param_parts}, got {result}")

                elif action_type == "FINAL_ANSWER":
                    print("Done")
                    break

                iteration = iteration + 1

if __name__ == "__main__":
    asyncio.run(main())
