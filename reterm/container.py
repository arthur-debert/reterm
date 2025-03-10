"""Container component for the reterm framework."""

from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from reterm.component import Component
from reterm.constants import Events


class Container(Component):
    """Container component that can hold and manage multiple child components.
    
    This class extends the base Component class to provide functionality for
    managing a hierarchy of components.
    """

    def __init__(self, id: Optional[str] = None, props: Optional[Dict[str, Any]] = None):
        """Initialize a container.
        
        Args:
            id: Optional unique identifier for the container.
            props: Optional properties for the container.
        """
        super().__init__(id, props)
        self._layout_direction = "vertical"  # "vertical" or "horizontal"
        self._layout_spacing = 0

    @property
    def layout_direction(self) -> str:
        """Get the layout direction."""
        return self._layout_direction
    
    @layout_direction.setter
    def layout_direction(self, direction: str):
        """Set the layout direction for child components.
        
        Args:
            direction: The layout direction, either "vertical" or "horizontal".
            
        Raises:
            ValueError: If the direction is not "vertical" or "horizontal".
        """
        if direction not in ["vertical", "horizontal"]:
            raise ValueError("Layout direction must be 'vertical' or 'horizontal'")
        
        self._layout_direction = direction
        self.update()
    
    def set_layout_direction(self, direction: str):
        """Set the layout direction for child components.
        
        Args:
            direction: The layout direction, either "vertical" or "horizontal".
        """
        self.layout_direction = direction

    @property
    def layout_spacing(self) -> int:
        """Get the spacing between child components."""
        return self._layout_spacing
    
    @layout_spacing.setter
    def layout_spacing(self, spacing: int):
        """Set the spacing between child components.
        
        Args:
            spacing: The spacing in cells.
        """
        self._layout_spacing = max(0, spacing)
        self.update()
    
    def set_layout_spacing(self, spacing: int):
        """Set the spacing between child components.
        
        Args:
            spacing: The spacing in cells.
        """
        self.layout_spacing = spacing

    def calculate_layout(self):
        """Calculate the layout for child components.
        
        This method calculates the position and size of each child component
        based on the container's layout direction and spacing.
        """
        if not self._children:
            return
        
        container_height, container_width = self.size
        start_y, start_x = self.position
        
        # Filter visible children
        visible_children = [child for child in self._children if child.visible]
        if not visible_children:
            return
        
        if self._layout_direction == "vertical":
            # Calculate available height per component
            total_spacing = self._layout_spacing * (len(visible_children) - 1)
            available_height = max(0, container_height - total_spacing)
            height_per_child = available_height // len(visible_children)
            
            # Position children vertically
            current_y = start_y
            for child in visible_children:
                child.set_position(current_y, start_x)
                child.set_size(height_per_child, container_width)
                current_y += height_per_child + self._layout_spacing
        else:  # horizontal
            # Calculate available width per component
            total_spacing = self._layout_spacing * (len(visible_children) - 1)
            available_width = max(0, container_width - total_spacing)
            width_per_child = available_width // len(visible_children)
            
            # Position children horizontally
            current_x = start_x
            for child in visible_children:
                child.set_position(start_y, current_x)
                child.set_size(container_height, width_per_child)
                current_x += width_per_child + self._layout_spacing

    def update(self):
        """Update the container and recalculate layout."""
        super().update()
        self.calculate_layout()

    def render(self):
        """Render the container and its children."""
        super().render()
        
        # Render children
        for child in self._children:
            if child.visible:
                child.render()

    def handle_event(self, event_name: str, *args, **kwargs) -> bool:
        """Handle an event and propagate it to children.
        
        Args:
            event_name: The name of the event.
            *args: Positional arguments for the event.
            **kwargs: Keyword arguments for the event.
            
        Returns:
            Whether the event was handled.
        """
        # Try to handle the event in this container
        handled = super().handle_event(event_name, *args, **kwargs)
        if handled:
            return True
        
        # If not handled, propagate to children
        for child in reversed(self._children):  # Reverse order for z-index (top-most first)
            if child.visible and child.handle_event(event_name, *args, **kwargs):
                return True
        
        return False


class VBox(Container):
    """Vertical box container."""
    
    def __init__(self, id: Optional[str] = None, props: Optional[Dict[str, Any]] = None):
        """Initialize a vertical box container.
        
        Args:
            id: Optional unique identifier for the container.
            props: Optional properties for the container.
        """
        super().__init__(id, props)
        self.layout_direction = "vertical"


class HBox(Container):
    """Horizontal box container."""
    
    def __init__(self, id: Optional[str] = None, props: Optional[Dict[str, Any]] = None):
        """Initialize a horizontal box container.
        
        Args:
            id: Optional unique identifier for the container.
            props: Optional properties for the container.
        """
        super().__init__(id, props)
        self.layout_direction = "horizontal"