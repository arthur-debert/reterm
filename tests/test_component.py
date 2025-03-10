"""Tests for the Component class."""

import pytest
from pytest import raises

from reterm.component import Component
from reterm.constants import ComponentState, Events


def test_component_initialization():
    """Test component initialization."""
    # Create a component without id or props
    component = Component()
    
    assert component.id is None
    assert component.props == {}
    assert component.lifecycle_state == ComponentState.CREATED
    assert component.parent is None
    assert component.children == []
    assert not component.is_mounted
    assert component.visible
    assert component.position == (0, 0)
    assert component.size == (0, 0)
    
    # Create a component with id and props
    component = Component(id="test", props={"key": "value"})
    
    assert component.id == "test"
    assert component.props == {"key": "value"}


def test_component_lifecycle():
    """Test component lifecycle methods."""
    component = Component()
    
    # Track lifecycle events
    events = []
    
    def handler(sender, **kwargs):
        events.append(sender.lifecycle_state)
    
    component.on(Events.MOUNT, handler)
    component.on(Events.UPDATE, handler)
    component.on(Events.UNMOUNT, handler)
    
    # Initial state
    assert component.lifecycle_state == ComponentState.CREATED
    assert not component.is_mounted
    
    # Mount
    component.mount()
    
    assert component.is_mounted
    assert component.lifecycle_state == ComponentState.MOUNTED
    assert events == [ComponentState.MOUNTED]
    
    # Update
    component.update()
    
    assert component.lifecycle_state == ComponentState.UPDATED
    assert events == [ComponentState.MOUNTED, ComponentState.UPDATED]
    
    # Unmount
    component.unmount()
    
    assert not component.is_mounted
    assert component.lifecycle_state == ComponentState.UNMOUNTED
    assert events == [ComponentState.MOUNTED, ComponentState.UPDATED, ComponentState.UNMOUNTED]


def test_component_state():
    """Test component state management."""
    component = Component()
    
    # Track update events
    updates = []
    
    def handler(sender, **kwargs):
        updates.append(True)
    
    component.on(Events.UPDATE, handler)
    
    # Mount the component so updates are triggered
    component.mount()
    
    # Set state
    component.state.set("key", "value")
    
    # Component should be updated
    assert len(updates) == 1
    assert component.state.get("key") == "value"


def test_component_position_size():
    """Test setting and getting component position and size."""
    component = Component()
    
    # Track update events
    updates = []
    
    def handler(sender, **kwargs):
        updates.append(True)
    
    component.on(Events.UPDATE, handler)
    
    # Mount the component so updates are triggered
    component.mount()
    
    # Set position
    component.position = (10, 20)
    
    assert component.position == (10, 20)
    assert len(updates) == 1
    
    # Set size
    component.size = (30, 40)
    
    assert component.size == (30, 40)
    assert len(updates) == 2


def test_component_visibility():
    """Test component visibility."""
    component = Component()
    
    # Track update events
    updates = []
    
    def handler(sender, **kwargs):
        updates.append(True)
    
    component.on(Events.UPDATE, handler)
    
    # Mount the component so updates are triggered
    component.mount()
    
    # Default visibility
    assert component.visible
    
    # Hide component
    component.visible = False
    
    assert not component.visible
    assert len(updates) == 1
    
    # Show component
    component.visible = True
    
    assert component.visible
    assert len(updates) == 2
    
    # Setting to the same value should not trigger update
    component.set_visible(True)
    
    assert len(updates) == 2


def test_component_parent_child():
    """Test parent-child relationships."""
    parent = Component(id="parent")
    child1 = Component(id="child1")
    child2 = Component(id="child2")
    
    # Add children
    parent.add_child(child1)
    parent.add_child(child2)
    
    # Check parent-child relationships
    assert child1.parent is parent
    assert child2.parent is parent
    assert parent.children == [child1, child2]
    
    # Remove a child
    parent.remove_child(child1)
    
    assert child1.parent is None
    assert parent.children == [child2]


def test_component_mount_unmount_hierarchy():
    """Test mounting and unmounting component hierarchies."""
    parent = Component(id="parent")
    child1 = Component(id="child1")
    child2 = Component(id="child2")
    
    # Add children
    parent.add_child(child1)
    parent.add_child(child2)
    
    # Mount parent
    parent.mount()
    
    # All components should be mounted
    assert parent.is_mounted
    assert child1.is_mounted
    assert child2.is_mounted
    
    # Add another child after mounting
    child3 = Component(id="child3")
    parent.add_child(child3)

    # New child should also be mounted
    assert child3.is_mounted
    
    # Unmount parent
    parent.unmount()
    
    # All components should be unmounted
    assert not parent.is_mounted
    assert not child1.is_mounted
    assert not child2.is_mounted
    assert not child3.is_mounted


def test_component_event_handling():
    """Test component event handling."""
    component = Component()
    
    # Track events
    events = []
    
    def handler(sender, **kwargs):
        events.append(kwargs.get("value"))
    
    # Register event handler
    component.on("custom_event", handler)
    
    # Handle event
    component.handle_event("custom_event", value="test")
    
    # Event should be emitted
    assert events == ["test"]


def test_component_name_uniqueness():
    """Test that components with the same name cannot be added to the same parent."""
    parent = Component()
    
    # Add a child with a name
    child1 = Component(props={"name": "test"})
    parent.add_child(child1)
    
    # Try to add another child with the same name
    child2 = Component(props={"name": "test"})
    with raises(ValueError, match="A child with name 'test' already exists"):
        parent.add_child(child2)
    
    # Add a child with a different name
    child3 = Component(props={"name": "other"})
    parent.add_child(child3)
    
    # Check that both children were added
    assert len(parent.children) == 2
    assert parent.children == [child1, child3]


def test_component_id_uniqueness():
    """Test that components with the same ID cannot be added to the component tree."""
    root = Component()
    
    # Add a child with an ID
    child1 = Component(id="test")
    root.add_child(child1)
    
    # Try to add another child with the same ID
    child2 = Component(id="test")
    with raises(ValueError, match="A component with ID 'test' already exists in the tree"):
        root.add_child(child2)
    
    # Create a deeper tree
    branch = Component()
    root.add_child(branch)
    
    # Try to add a component with the same ID to a different branch
    child3 = Component(id="test")
    with raises(ValueError, match="A component with ID 'test' already exists in the tree"):
        branch.add_child(child3)
    
    # Add a child with a different ID
    child4 = Component(id="other")
    branch.add_child(child4)


def test_component_id_uniqueness_in_subtrees():
    """Test that components with the same ID cannot be added even in nested subtrees."""
    root = Component()
    
    # Create a nested structure
    branch1 = Component()
    branch2 = Component()
    subbranch = Component()
    
    # Add branches to root
    root.add_child(branch1)
    root.add_child(branch2)
    
    # Add subbranch to branch2
    branch2.add_child(subbranch)
    
    # Add a component with ID to branch1
    child1 = Component(id="unique")
    branch1.add_child(child1)
    
    # Create a subtree with a component with the same ID
    subtree_root = Component()
    subtree_child = Component(id="unique")
    subtree_root.add_child(subtree_child)
    
    # Try to add the subtree to subbranch
    with raises(ValueError, match="A component with ID 'unique' already exists in the tree"):
        subbranch.add_child(subtree_root)