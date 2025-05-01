iteration = 0
memory_log = []

def reset_memory():
    global iteration, memory_log
    iteration = 0
    memory_log = [] 

def update_memory(entry: str):
    global iteration, memory_log
    print("in update memory")
    memory_log.append(entry)
    iteration += 1

def get_memory_log() -> list[str]:
    return memory_log
