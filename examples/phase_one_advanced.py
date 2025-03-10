#!/usr/bin/env python3
"""
Advanced reterm example demonstrating more complex features of Phase I.

This example shows:
- Complex component hierarchy
- Layout management with VBox and HBox
- Event propagation
- Global state management
- Component visibility control
- Custom event handling
"""

from reterm import Component, Container, VBox, HBox, EventBus, Events, StateManager


class Label(Component):
    """A simple label component."""
    
    def __init__(self, id=None, props=None):
        super().__init__(id, props)
        self.text = props.get("text", "") if props else ""
    
    def render(self):
        """Render the label."""
        super().render()
        print(f"[Label] {self.text}")


class TextInput(Component):
    """A text input component."""
    
    def __init__(self, id=None, props=None):
        super().__init__(id, props)
        self.label = props.get("label", "") if props else ""
        self.state.set("value", props.get("value", "") if props else "")
        self.state.set("focused", False)
    
    @property
    def value(self):
        """Get the current value."""
        return self.state.get("value")
    
    @value.setter
    def value(self, new_value):
        """Set the value and emit change event."""
        self.state.set("value", new_value)
        self.emit("change", value=new_value)
    
    def focus(self):
        """Focus the input."""
        self.state.set("focused", True)
        self.emit("focus")
    
    def blur(self):
        """Blur the input."""
        self.state.set("focused", False)
        self.emit("blur")
    
    def handle_event(self, event_name, *args, **kwargs):
        """Handle input events."""
        if event_name == "input":
            self.value = kwargs.get("value", "")
            return True
        elif event_name == "focus":
            self.focus()
            return True
        elif event_name == "blur":
            self.blur()
            return True
        return super().handle_event(event_name, *args, **kwargs)
    
    def render(self):
        """Render the text input."""
        super().render()
        focused = "*" if self.state.get("focused") else " "
        print(f"[TextInput{focused}] {self.label}: {self.value}")


class Button(Component):
    """A button component."""
    
    def __init__(self, id=None, props=None):
        super().__init__(id, props)
        self.label = props.get("label", "Button") if props else "Button"
        self.state.set("disabled", props.get("disabled", False) if props else False)
    
    @property
    def disabled(self):
        """Get the disabled state."""
        return self.state.get("disabled")
    
    @disabled.setter
    def disabled(self, value):
        """Set the disabled state."""
        self.state.set("disabled", value)
    
    def handle_event(self, event_name, *args, **kwargs):
        """Handle button events."""
        if event_name == "click" and not self.disabled:
            print(f"Button '{self.label}' clicked!")
            if self.props and "on_click" in self.props and callable(self.props["on_click"]):
                self.props["on_click"]()
            return True
        return super().handle_event(event_name, *args, **kwargs)
    
    def render(self):
        """Render the button."""
        super().render()
        disabled = " (disabled)" if self.disabled else ""
        print(f"[Button] {self.label}{disabled}")


class Form(VBox):
    """A form container with validation."""
    
    def __init__(self, id=None, props=None):
        super().__init__(id, props)
        self.state.set("valid", False)
        self.state.set("submitted", False)
        self.layout_spacing = 1
    
    def validate(self):
        """Validate all form fields."""
        # In a real app, this would check all inputs
        valid = True
        for child in self.children:
            if isinstance(child, TextInput) and not child.value:
                valid = False
                break
        
        self.state.set("valid", valid)
        return valid
    
    def submit(self):
        """Submit the form if valid."""
        if self.validate():
            self.state.set("submitted", True)
            self.emit("submit")
            return True
        else:
            print("Form validation failed!")
            return False
    
    def reset(self):
        """Reset the form."""
        self.state.set("submitted", False)
        for child in self.children:
            if isinstance(child, TextInput):
                child.value = ""
    
    def handle_event(self, event_name, *args, **kwargs):
        """Handle form events."""
        if event_name == "submit":
            return self.submit()
        elif event_name == "reset":
            self.reset()
            return True
        return super().handle_event(event_name, *args, **kwargs)


class Notification(Component):
    """A notification component that can be shown/hidden."""
    
    def __init__(self, id=None, props=None):
        super().__init__(id, props)
        self.message = props.get("message", "") if props else ""
        self.type = props.get("type", "info") if props else "info"  # info, success, error
        self.visible = props.get("visible", False) if props else False
        self.state.set("timeout", props.get("timeout", 3) if props else 3)  # seconds
    
    def show(self, message=None, type=None):
        """Show the notification."""
        if message:
            self.message = message
        if type:
            self.type = type
        self.visible = True
        print(f"Notification shown: {self.message} ({self.type})")
    
    def hide(self):
        """Hide the notification."""
        self.visible = False
        print("Notification hidden")
    
    def render(self):
        """Render the notification if visible."""
        if not self.visible:
            return
        
        super().render()
        print(f"[{self.type.upper()}] {self.message}")


class AdvancedApp(Container):
    """An advanced application with form, notifications, and global state."""
    
    def __init__(self):
        super().__init__(id="advanced_app")
        
        # Set up global event bus and state manager
        self.event_bus = EventBus()
        self.state_manager = StateManager()
        
        # Create global app state
        self.app_state = self.state_manager.create_state("app", {
            "user": None,
            "theme": "light",
            "notifications": []
        })
        
        # Create main layout
        self.main_layout = VBox(id="main_layout")
        self.main_layout.layout_spacing = 2
        
        # Create header
        self.header = HBox(id="header")
        self.title = Label(id="title", props={"text": "Advanced reterm Example"})
        self.header.add_child(self.title)
        
        # Create form
        self.form = Form(id="user_form")
        self.name_input = TextInput(id="name_input", props={"label": "Name"})
        self.email_input = TextInput(id="email_input", props={"label": "Email"})
        
        # Create form buttons in a horizontal layout
        self.form_buttons = HBox(id="form_buttons")
        self.form_buttons.layout_spacing = 2
        
        self.submit_button = Button(id="submit_button", props={
            "label": "Submit",
            "on_click": self.handle_submit
        })
        
        self.reset_button = Button(id="reset_button", props={
            "label": "Reset",
            "on_click": self.handle_reset
        })
        
        self.form_buttons.add_child(self.submit_button)
        self.form_buttons.add_child(self.reset_button)
        
        # Add inputs and buttons to form
        self.form.add_child(self.name_input)
        self.form.add_child(self.email_input)
        self.form.add_child(self.form_buttons)
        
        # Create notification area
        self.notification = Notification(id="notification")
        
        # Create result area (initially hidden)
        self.result_area = VBox(id="result_area")
        self.result_area.visible = False
        
        self.result_title = Label(id="result_title", props={"text": "Submission Result:"})
        self.result_name = Label(id="result_name")
        self.result_email = Label(id="result_email")
        
        self.back_button = Button(id="back_button", props={
            "label": "Back to Form",
            "on_click": self.show_form
        })
        
        self.result_area.add_child(self.result_title)
        self.result_area.add_child(self.result_name)
        self.result_area.add_child(self.result_email)
        self.result_area.add_child(self.back_button)
        
        # Add components to main layout
        self.main_layout.add_child(self.header)
        self.main_layout.add_child(self.notification)
        self.main_layout.add_child(self.form)
        self.main_layout.add_child(self.result_area)
        
        # Add main layout to app
        self.add_child(self.main_layout)
        
        # Set up event listeners
        self.event_bus.on("form_submitted", self.handle_form_submitted)
        
        # Set layout properties
        self.size = (24, 80)  # height, width
    
    def handle_submit(self):
        """Handle form submission."""
        if self.form.submit():
            user_data = {
                "name": self.name_input.value,
                "email": self.email_input.value
            }
            
            # Update global state
            self.app_state.set("user", user_data)
            
            # Show success notification
            self.notification.show(
                message="Form submitted successfully!",
                type="success"
            )
            
            # Emit event on the event bus
            self.event_bus.emit("form_submitted", user=user_data)
            
            # Show result area
            self.show_results()
    
    def handle_reset(self):
        """Handle form reset."""
        self.form.handle_event("reset")
        self.notification.show(
            message="Form has been reset.",
            type="info"
        )
    
    def handle_form_submitted(self, sender, user=None):
        """Handle form submitted event from event bus."""
        print(f"Event bus received form_submitted event with user: {user}")
    
    def show_results(self):
        """Show the results area and hide the form."""
        user = self.app_state.get("user")
        if user:
            self.result_name.text = f"Name: {user['name']}"
            self.result_email.text = f"Email: {user['email']}"
        
        self.form.visible = False
        self.result_area.visible = True
    
    def show_form(self):
        """Show the form and hide the results area."""
        self.form.visible = True
        self.result_area.visible = False
    
    def render(self):
        """Render the app."""
        print("\n=== Advanced reterm Example ===")
        super().render()
        print("==============================\n")


def run():
    """Create and return the app instance.
    
    This function is called by the runner.
    
    Returns:
        AdvancedApp: The app instance.
    """
    # Create the app
    app = AdvancedApp()
    return app


def simulate(app):
    """Simulate user interactions with the app.
    
    This function is called by the runner after mounting and rendering the app.
    
    Args:
        app: The app instance.
    """
    # Simulate user interaction
    print("\n--- User interaction simulation ---")
    
    # Focus and input name
    app.name_input.handle_event("focus")
    app.name_input.handle_event("input", value="John Doe")
    app.name_input.handle_event("blur")
    
    # Focus and input email
    app.email_input.handle_event("focus")
    app.email_input.handle_event("input", value="john@example.com")
    app.email_input.handle_event("blur")
    
    # Render after inputs
    app.render()
    
    # Submit the form
    app.submit_button.handle_event("click")
    
    # Render after submission
    app.render()
    
    # Go back to form
    app.back_button.handle_event("click")
    
    # Render after going back
    app.render()
    
    # Reset the form
    app.reset_button.handle_event("click")
    
    # Final render
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