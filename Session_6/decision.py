import json

def interpret_response(response: str):
    print("in interpret_response")
    response = response.strip()
    print("response of interpret is", response)

    if response.startswith("{"):
        # Assume it's JSON
        try:
            data = json.loads(response)
            if data.get("type") == "FUNCTION_CALL":
                func_name = data.get("tool")
                args = [f"{k}={v}" for k, v in data.get("args", {}).items()]
                return "FUNCTION_CALL", (func_name, args)
            elif data.get("type") == "FINAL_ANSWER":
                return "FINAL_ANSWER", data.get("answer", "")
        except Exception as e:
            print("JSON parsing error:", e)
            return None, None

    if response.startswith("FUNCTION_CALL:"):
        _, call = response.split(":", 1)
        parts = [p.strip() for p in call.split("|")]
        return "FUNCTION_CALL", (parts[0], parts[1:])
    elif response.startswith("FINAL_ANSWER:"):
        return "FINAL_ANSWER", response.split(":", 1)[1].strip()

    return None, None

