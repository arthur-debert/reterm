"""Base component class for the reterm framework."""

from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union, cast

from reterm.constants import ComponentState, Events
from reterm.events import EventEmitter
from reterm.state import State


class Component(EventEmitter):
    """Base class for all UI components.
    
    This class provides the foundation for all UI components in the reterm framework.
    It includes lifecycle methods, event handling, and state management.
    """

    def __init__(self, id: Optional[str] = None, props: Optional[Dict[str, Any]] = None):
        """Initialize a component.
        
        Args:
            id: Optional unique identifier for the component.
            props: Optional properties for the component.
        """
        super().__init__()
        self.id = id
        self.props = props or {}
        self.name = props.get("name") if props else None
        self.state = State()
        self._lifecycle_state = ComponentState.CREATED
        self._parent = None
        self._children = []
        self._is_mounted = False
        self._is_visible = True
        self._position = (0, 0)  # (y, x) coordinates
        self._size = (0, 0)      # (height, width)
        
        # Register state change handler
        self.state.on(Events.STATE_CHANGE, self._handle_state_change)
        
        # Emit init event
        self.emit(Events.INIT)

    @property
    def root(self):
        """Get the root component of the tree.
        
        Returns:
            The root component.
        """
        current = self
        while current._parent is not None:
            current = current._parent
        return current
    
    def find_by_id(self, id: str) -> Optional['Component']:
        """Find a component by ID in the subtree.
        
        Args:
            id: The ID to search for.
            
        Returns:
            The component with the given ID, or None if not found.
        """
        if self.id == id:
            return self
        for child in self._children:
            found = child.find_by_id(id)
            if found is not None:
                return found
        return None

    def _handle_state_change(self, sender, **kwargs):
        """Handle state changes and trigger updates.
        
        Args:
            sender: The state object that emitted the event.
            **kwargs: Event data, which may include:
                key, value, old_value: For single value changes.
                keys, updates: For batch updates.
        """
        if self._is_mounted:
            self.update()

    def mount(self):
        """Mount the component.
        
        This method is called when the component is added to the DOM.
        Override this method to perform initialization that requires DOM nodes.
        """
        if not self._is_mounted:
            self._is_mounted = True
            self._lifecycle_state = ComponentState.MOUNTED
            self.emit(Events.MOUNT)
            
            # Mount children
            for child in self._children:
                child.mount()

    def unmount(self):
        """Unmount the component.
        
        This method is called when the component is removed from the DOM.
        Override this method to perform cleanup.
        """
        if self._is_mounted:
            # Unmount children first
            for child in self._children:
                child.unmount()
                
            self._is_mounted = False
            self._lifecycle_state = ComponentState.UNMOUNTED
            self.emit(Events.UNMOUNT)

    def update(self):
        """Update the component.
        
        This method is called when the component's state or props change.
        Override this method to perform updates based on the new state or props.
        """
        if self._is_mounted:
            self._lifecycle_state = ComponentState.UPDATED
            self.emit(Events.UPDATE)
            self.render()

    def render(self):
        """Render the component.
        
        This method is responsible for rendering the component to the screen.
        Override this method to define the component's appearance.
        """
        self.emit(Events.RENDER)
        # Base implementation does nothing, subclasses should override

    @property
    def parent(self):
        """Get the parent component."""
        return self._parent
    
    @parent.setter
    def parent(self, value):
        """Set the parent component."""
        self._parent = value

    def add_child(self, child):
        """Add a child component.
        
        Args:
            child: The child component to add.
            
        Raises:
            ValueError: If a child with the same name already exists, or
                        if a component with the same ID already exists in the tree.
        """
        if child not in self._children:
            # Check for duplicate name within the same parent
            if child.name is not None:
                for existing_child in self._children:
                    if existing_child.name == child.name:
                        raise ValueError(f"A child with name '{child.name}' already exists")
            
            # Check for duplicate ID in the entire tree
            if child.id is not None:
                root = self.root
                existing = root.find_by_id(child.id)
                if existing is not None:
                    raise ValueError(f"A component with ID '{child.id}' already exists in the tree")
            
            # Check for duplicate IDs in the subtree being added
            descendants = child._get_all_descendants()
            for descendant in descendants:
                if descendant.id is not None:
                    # Check if this ID exists in the current tree
                    root = self.root
                    existing = root.find_by_id(descendant.id)
                    if existing is not None:
                        raise ValueError(
                            f"A component with ID '{descendant.id}' already exists in the tree")
            
            self._children.append(child)
            child.parent = self
            # If this component is already mounted, mount the child too
            if self.is_mounted:
                child.mount()

    def remove_child(self, child):
        """Remove a child component.
        
        Args:
            child: The child component to remove.
        """
        if child in self._children:
            # Unmount the child if this component is mounted
            if self.is_mounted:
                child.unmount()
            
            self._children.remove(child)
            child.parent = None

    def _get_all_descendants(self) -> List['Component']:
        """Get all descendant components recursively.
        
        Returns:
            List of all descendant components.
        """
        descendants = []
        for child in self._children:
            descendants.append(child)
            descendants.extend(child._get_all_descendants())
        return descendants

    @property
    def children(self):
        """Get all child components."""
        return self._children.copy()

    @property
    def position(self) -> Tuple[int, int]:
        """Get the component's position as (y, x) coordinates."""
        return self._position
    
    @position.setter
    def position(self, value: Tuple[int, int]):
        """Set the component's position as (y, x) coordinates."""
        self._position = value
        if self.is_mounted:
            self.update()
    
    def set_position(self, y: int, x: int):
        """Set the component's position.
        
        Args:
            y: Y coordinate (row).
            x: X coordinate (column).
        """
        self.position = (y, x)

    @property
    def size(self) -> Tuple[int, int]:
        """Get the component's size as (height, width)."""
        return self._size
    
    @size.setter
    def size(self, value: Tuple[int, int]):
        """Set the component's size as (height, width)."""
        self._size = value
        if self.is_mounted:
            self.update()
    
    def set_size(self, height: int, width: int):
        """Set the component's size.
        
        Args:
            height: Height in rows.
            width: Width in columns.
        """
        self.size = (height, width)

    @property
    def visible(self) -> bool:
        """Get whether the component is visible."""
        return self._is_visible
    
    @visible.setter
    def visible(self, value: bool):
        """Set whether the component is visible."""
        if self._is_visible != value:
            self._is_visible = value
            if self.is_mounted:
                self.update()
    
    def set_visible(self, visible: bool):
        """Set whether the component is visible.
        
        Args:
            visible: Whether the component should be visible.
        """
        self.visible = visible

    @property
    def is_mounted(self) -> bool:
        """Check if the component is mounted."""
        return self._is_mounted

    @property
    def lifecycle_state(self) -> str:
        """Get the component's lifecycle state."""
        return self._lifecycle_state

    def handle_event(self, event_name: str, *args, **kwargs) -> bool:
        """Handle an event.
        
        This method is called when an event is propagated to this component.
        Override this method to handle specific events.
        
        Args:
            event_name: The name of the event.
            *args: Positional arguments for the event.
            **kwargs: Keyword arguments for the event.
            
        Returns:
            Whether the event was handled.
        """
        # Emit the event on this component
        self.emit(event_name, *args, **kwargs)
        
        # Base implementation doesn't handle any events
        return False