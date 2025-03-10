#!/usr/bin/env python3
"""
Runner script for reterm examples.

Usage:
    ./runner.py <example_name>

Example:
    ./runner.py phase_one_simple
"""

import sys
import importlib
import os


def list_examples():
    """List all available examples."""
    examples = []
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith('.py') and filename != 'runner.py' and filename != '__init__.py':
            example_name = filename[:-3]  # Remove .py extension
            examples.append(example_name)
    return sorted(examples)


def run_example(example_name):
    """Run the specified example."""
    try:
        # Import the example module
        module_name = f"examples.{example_name}"
        example_module = importlib.import_module(module_name)
        
        # Check if the module has a run function
        if not hasattr(example_module, 'run'):
            print(f"Error: Example '{example_name}' does not have a run() function.")
            return False
        
        # Run the example
        print(f"Running example: {example_name}")
        print("=" * 50)
        
        app = example_module.run()
        
        # Mount the app
        app.mount()
        
        # Render the initial state
        app.render()
        
        # Run the example's simulation
        if hasattr(example_module, 'simulate'):
            example_module.simulate(app)
        
        # Unmount the app
        app.unmount()
        print("App unmounted")
        
        print("=" * 50)
        print(f"Example '{example_name}' completed successfully.")
        return True
        
    except ImportError:
        print(f"Error: Example '{example_name}' not found.")
        return False
    except Exception as e:
        print(f"Error running example '{example_name}': {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: ./runner.py <example_name>")
        print("\nAvailable examples:")
        for example in list_examples():
            print(f"  - {example}")
        return
    
    example_name = sys.argv[1]
    run_example(example_name)


if __name__ == "__main__":
    main()