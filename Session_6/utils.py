import os
import ast
import openai
from dotenv import load_dotenv
import asyncio

load_dotenv()
import os

os.environ["OPENAI_API_KEY"] = ""  # Replace with your actual API key
openai.api_key = os.getenv("OPENAI_API_KEY")
from openai import OpenAI


client = OpenAI(api_key=openai.api_key) 

def parse_function_call_params(param_parts):
    result = {}
    for part in param_parts:
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        try:
            value = ast.literal_eval(value)
        except Exception:
            value = value.strip()
        keys = key.split(".")
        current = result
        for k in keys[:-1]:
            current = current.setdefault(k, {})
        current[keys[-1]] = value
    return result

async def call_openai(prompt, model="gpt-3.5-turbo", timeout=10):
    loop = asyncio.get_event_loop()
    response = await asyncio.wait_for(
        loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
        ),
        timeout=timeout
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content



def validate_against_schema(tool, parsed_args):
    expected_schema = tool.inputSchema['properties']
    for field in tool.inputSchema.get('required', []):
        if field not in parsed_args:
            raise ValueError(f"Missing required field: {field}")

    for key, schema_info in expected_schema.items():
        if key in parsed_args:
            expected_type = schema_info['type']
            value = parsed_args[key]
            if expected_type == "string" and not isinstance(value, str):
                parsed_args[key] = str(value)
            elif expected_type == "integer" and not isinstance(value, int):
                raise ValueError(f"Field {key} must be an integer.")
            elif expected_type == "array" and not isinstance(value, list):
                raise ValueError(f"Field {key} must be a list.")
    return parsed_args


