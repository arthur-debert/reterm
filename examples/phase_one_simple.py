#!/usr/bin/env python3
"""
Simple reterm example demonstrating basic features of Phase I.

This example shows:
- Creating components
- Building a component hierarchy
- Handling events
- Managing component state
"""

from reterm import Component, Container, VBox, HBox, Events


class Button(Component):
    """A simple button component."""
    
    def __init__(self, id=None, props=None):
        super().__init__(id, props)
        self.label = props.get("label", "Button")
    
    def render(self):
        """Render the button."""
        super().render()
        print(f"[Button] {self.label}")
    
    def handle_event(self, event_name, *args, **kwargs):
        """Handle button events."""
        if event_name == "click":
            print(f"Button '{self.label}' clicked!")
            if "on_click" in self.props and callable(self.props["on_click"]):
                self.props["on_click"]()
            return True
        return super().handle_event(event_name, *args, **kwargs)


class SimpleApp(Container):
    """A simple application with a button."""
    
    def __init__(self):
        super().__init__(id="simple_app")
        
        # Create a counter in the state
        self.state.set("counter", 0)
        
        # Create a button
        self.button = Button(id="increment_button", props={
            "label": "Increment Counter",
            "on_click": self.increment_counter
        })
        
        # Add the button to the app
        self.add_child(self.button)
    
    def increment_counter(self):
        """Increment the counter when the button is clicked."""
        current_count = self.state.get("counter")
        self.state.set("counter", current_count + 1)
        print(f"Counter incremented to: {current_count + 1}")
    
    def render(self):
        """Render the app."""
        print("\n--- Simple App ---")
        print(f"Counter: {self.state.get('counter')}")
        super().render()
        print("-----------------\n")


def run():
    """Create and return the app instance.
    
    This function is called by the runner.
    
    Returns:
        SimpleApp: The app instance.
    """
    # Create the app
    app = SimpleApp()
    return app


def simulate(app):
    """Simulate user interactions with the app.
    
    This function is called by the runner after mounting and rendering the app.
    
    Args:
        app: The app instance.
    """
    # Simulate clicking the button 3 times
    for _ in range(3):
        app.button.handle_event("click")
        app.render()


def main():
    """Run the example directly."""
    app = run()
    app.mount()
    app.render()
    simulate(app)
    app.unmount()
    print("App unmounted")
    


if __name__ == "__main__":
    main()