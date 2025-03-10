"""Constants for the reterm framework."""

# Event names
class Events:
    """Event names used throughout the framework."""
    # Lifecycle events
    INIT = "init"
    MOUNT = "mount"
    UNMOUNT = "unmount"
    UPDATE = "update"
    
    # Input events
    KEY_PRESS = "key_press"
    MOUSE_CLICK = "mouse_click"
    MOUSE_MOVE = "mouse_move"
    
    # Window events
    RESIZE = "resize"
    FOCUS = "focus"
    BLUR = "blur"
    
    # Component events
    RENDER = "render"
    STATE_CHANGE = "state_change"

# Component states
class ComponentState:
    """Component state constants."""
    CREATED = "created"
    MOUNTED = "mounted"
    UPDATED = "updated"
    UNMOUNTED = "unmounted"