"""Tests for the Container class."""

import pytest

from reterm.container import Container, VBox, HBox
from reterm.component import Component


def test_container_initialization():
    """Test container initialization."""
    # Create a container without id or props
    container = Container()
    
    assert container.id is None
    assert container.props == {}
    assert container.layout_direction == "vertical"
    assert container.layout_spacing == 0
    
    # Create a container with id and props
    container = Container(id="test", props={"key": "value"})
    
    assert container.id == "test"
    assert container.props == {"key": "value"}


def test_container_layout_direction():
    """Test setting and getting layout direction."""
    container = Container()
    
    # Default direction
    assert container.layout_direction == "vertical"
    
    # Set direction
    container.layout_direction = "horizontal"
    
    assert container.layout_direction == "horizontal"
    
    # Invalid direction
    with pytest.raises(ValueError):
        container.layout_direction = "invalid"


def test_container_layout_spacing():
    """Test setting and getting layout spacing."""
    container = Container()
    
    # Default spacing
    assert container.layout_spacing == 0
    
    # Set spacing
    container.layout_spacing = 10
    
    assert container.layout_spacing == 10
    
    # Negative spacing should be clamped to 0
    container.layout_spacing = -5
    
    assert container.layout_spacing == 0


def test_container_calculate_layout_vertical():
    """Test calculating vertical layout."""
    container = Container()
    container.size = (100, 200)
    container.position = (0, 0)
    
    # Add children
    child1 = Component(id="child1")
    child2 = Component(id="child2")
    container.add_child(child1)
    container.add_child(child2)
    
    # Calculate layout
    container.calculate_layout()
    
    # Children should be positioned vertically
    assert child1.position == (0, 0)
    assert child1.size == (50, 200)
    assert child2.position == (50, 0)
    assert child2.size == (50, 200)
    
    # Add spacing
    container.layout_spacing = 10
    container.calculate_layout()
    
    # Children should be positioned with spacing
    assert child1.position == (0, 0)
    assert child1.size == (45, 200)  # (100 - 10) / 2 = 45
    assert child2.position == (55, 0)  # 45 + 10 = 55
    assert child2.size == (45, 200)


def test_container_calculate_layout_horizontal():
    """Test calculating horizontal layout."""
    container = Container()
    container.layout_direction = "horizontal"
    container.size = (100, 200)
    container.position = (0, 0)
    
    # Add children
    child1 = Component(id="child1")
    child2 = Component(id="child2")
    container.add_child(child1)
    container.add_child(child2)
    
    # Calculate layout
    container.calculate_layout()
    
    # Children should be positioned horizontally
    assert child1.position == (0, 0)
    assert child1.size == (100, 100)
    assert child2.position == (0, 100)
    assert child2.size == (100, 100)
    
    # Add spacing
    container.layout_spacing = 10
    container.calculate_layout()
    
    # Children should be positioned with spacing
    assert child1.position == (0, 0)
    assert child1.size == (100, 95)  # (200 - 10) / 2 = 95
    assert child2.position == (0, 105)  # 95 + 10 = 105
    assert child2.size == (100, 95)


def test_container_calculate_layout_visibility():
    """Test layout calculation with visibility."""
    container = Container()
    container.size = (100, 200)
    container.position = (0, 0)
    
    # Add children
    child1 = Component(id="child1")
    child2 = Component(id="child2")
    child3 = Component(id="child3")
    container.add_child(child1)
    container.add_child(child2)
    container.add_child(child3)
    
    # Hide one child
    child2.visible = False
    
    # Calculate layout
    container.calculate_layout()
    
    # Only visible children should be positioned
    assert child1.position == (0, 0)
    assert child1.size == (50, 200)
    assert child3.position == (50, 0)
    assert child3.size == (50, 200)


def test_container_event_propagation():
    """Test event propagation to children."""
    container = Container()
    child1 = Component(id="child1")
    child2 = Component(id="child2")
    
    container.add_child(child1)
    container.add_child(child2)
    
    # Track events
    events = []
    
    # Override handle_event to track calls
    original_handle_event = Component.handle_event
    
    def mock_handle_event(self, event_name, *args, **kwargs):
        events.append((self.id, event_name))
        return original_handle_event(self, event_name, *args, **kwargs)
    
    # Apply mock to all components
    Component.handle_event = mock_handle_event
    
    try:
        # Handle event
        container.handle_event("test_event")
        
        # Event should be propagated to all children
        assert events == [(None, "test_event"), ("child2", "test_event"), ("child1", "test_event")]
    finally:
        # Restore original method
        Component.handle_event = original_handle_event


def test_vbox_initialization():
    """Test VBox initialization."""
    vbox = VBox()
    
    assert vbox.layout_direction == "vertical"


def test_hbox_initialization():
    """Test HBox initialization."""
    hbox = HBox()
    
    assert hbox.layout_direction == "horizontal"