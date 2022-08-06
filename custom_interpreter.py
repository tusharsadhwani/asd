"""
Custom Interpreter implementation for Python code.

Lets you design DSLs or other wacky Python scripts, as long as they are valid
Python syntax. You do this by controlling how the Python source gets converted
to a code object, everytime a command is entered in the REPL.

By modifying the source using any means possible, eg. regex, but more commonly,
by parsing it and doing AST manipulation, you can essentially transform your
code to make it do whatever you want.

For an example, look at the library zxpy: https://github.com/tusharsadhwani/zxpy
"""

import ast
import code
from contextlib import suppress
import sys


class CursedConsole(code.InteractiveConsole):
    def runsource(
        self,
        source: str,
        filename: str = "<input>",
        symbol: str = "single",
    ) -> bool:
        # First, check if it could be incomplete input, return True if it is.
        # This will allow it to keep taking input
        with suppress(SyntaxError, OverflowError):
            if code.compile_command(source) == None:
                return True

        try:
            # In this block, you can do whatever you want.
            # Just make sure to create a code object at the end.
            tree = ast.parse(source)
            code_obj = compile(tree, filename, "exec")
        except (ValueError, SyntaxError):
            # Let the original implementation take care of incomplete input / errors
            return super().runsource(source, filename, symbol)

        self.runcode(code_obj)
        return False


CursedConsole().interact(banner=f"My Custom REPL, {sys.version}", exitmsg="")
