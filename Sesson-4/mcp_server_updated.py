# basic import 

from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
from pywinauto.application import Application
import win32gui
import win32con
import time
from win32api import GetSystemMetrics

# instantiate an MCP server client
mcp = FastMCP("Calculator")
# Global paint state
paint_app = None
last_drawn_rect = None  # (x1, y1, x2, y2)


# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]


from win32api import GetSystemMetrics
import time





@mcp.tool("draw_rectangle")
async def draw_rectangle(position: str = "center") -> dict:
    """Draw a rectangle in Paint using a semantic position like 'center', 'top-left', etc."""
    global paint_app
    try:
        if not paint_app:
            return {
                "content": ["Paint is not open. Please call open_paint first."]
            }

        paint_window = paint_app.window(class_name='MSPaintApp')

        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.2)

        # Click Rectangle Tool
        paint_window.click_input(coords=(523, 82))
        time.sleep(0.3)

        # Get canvas and its size
        canvas = paint_window.child_window(class_name='MSPaintView')
        canvas_rect = canvas.rectangle()
        width = canvas_rect.width()
        height = canvas_rect.height()
        left = canvas_rect.left
        top = canvas_rect.top

        # Calculate rectangle coordinates based on position
        if position.lower() == "center":
            x1 = left + width // 2 - 200
            y1 = top + height // 2 - 100
            x2 = left + width // 2 + 190
            y2 = top + height // 2 + 100
        elif position.lower() in ["top-left", "topleft"]:
            x1, y1 = left + 20, top + 20
            x2, y2 = x1 + 200, y1 + 100
        elif position.lower() in ["bottom-right", "bottomright"]:
            x2, y2 = left + width - 20, top + height - 20
            x1, y1 = x2 - 200, y2 - 100
        else:
            return {
                "content": ["Unknown position '{position}'. Use 'center', 'top-left', or 'bottom-right'."]
            }

        # Draw rectangle
        canvas.press_mouse_input(coords=(x1, y1))
        canvas.move_mouse_input(coords=(x2, y2))
        canvas.release_mouse_input(coords=(x2, y2))

        global last_drawn_rect
        last_drawn_rect = (x1, y1, x2, y2)


        return {
            "content": [TextContent(type="text", text=f"Rectangle drawn at position: {position}")]
        }

    except Exception as e:
        return {
            "content": [TextContent(type="text", text=f"Error drawing rectangle: {str(e)}")]
        }

from typing import List, Union

@mcp.tool("int_list_to_exponential_sum")
def int_list_to_exponential_sum(int_list: List[Union[int, float, str]]) -> float:
    """
    Calculate the exponential of each number in the list and return the sum.
    
    Args:
        int_list: A list of numbers (as integers, floats, or strings)
        
    Returns:
        The sum of exponentials of all numbers in the list
    """
    if not int_list:
        return 0.0
    
    # Convert all values to float
    converted_list = []
    for item in int_list:
        if isinstance(item, (int, float)):
            converted_list.append(float(item))
        elif isinstance(item, str):
            # Remove any non-numeric characters
            cleaned = item.strip()
            if cleaned:
                converted_list.append(float(cleaned))
        else:
            raise ValueError(f"Cannot convert {item} of type {type(item)} to float")
    
    # Calculate exponentials and sum
    try:
        total = sum(math.exp(num) for num in converted_list)
        return total
    except OverflowError:
        # Handle very large numbers
        return float('inf')


@mcp.tool("add_text_in_paint")
async def add_text_in_paint(text: str) -> dict:
    """
        This function adds text to the rectangle drawn in the paint.
        Arguments: text: str
        Returns: A message indicating that text has been added to the paint.
    """
    global paint_app
    try:
        if not paint_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paint is not open. Please call open_paint first."
                    )
                ]
            }
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Ensure Paint window is active
        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.5)
        
        # Click on the Rectangle tool
        #paint_window.click_input(coords=(528, 92))
        time.sleep(0.5)
        
        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        # Select text tool using keyboard shortcuts
        # Activate the Text tool using Alt+H, T
        paint_window.type_keys('%h', pause=0.2)
        time.sleep(0.4)
        paint_window.type_keys('t', pause=0.2)
        time.sleep(0.4)

        # Click where to start typing
        canvas_rect = canvas.rectangle()
        x = (canvas_rect.left + canvas_rect.right) // 2 -200
        y = (canvas_rect.top + canvas_rect.bottom) // 2 -100
        canvas.click_input(coords=(x, y))

        time.sleep(0.5)
        
        # Type the text passed from client
        paint_window.type_keys(text, with_spaces=True)

        time.sleep(0.5)
        
        # Click to exit text mode
        canvas.click_input(coords=(1050, 800))
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Text:'{text}' added successfully"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        }




@mcp.tool("open_paint")
async def open_paint() -> dict:
    """Open Microsoft Paint maximized on secondary monitor"""
    global paint_app
    try:
        paint_app = Application().start('mspaint.exe')
        time.sleep(0.2)
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Get primary monitor width
        primary_width = GetSystemMetrics(0)
        
        # First move to secondary monitor without specifying size
        win32gui.SetWindowPos(
            paint_window.handle,
            win32con.HWND_TOP,
            0, 0,  # Position it on secondary monitor
            0, 0,  # Let Windows handle the size
            win32con.SWP_NOSIZE  # Don't change the size
        )
        
        # Now maximize the window
        win32gui.ShowWindow(paint_window.handle, win32con.SW_MAXIMIZE)
        time.sleep(0.2)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Paint opened successfully on secondary monitor and maximized"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Paint: {str(e)}"
                )
            ]
        }
# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
