import pytest

from src.graph import Node, NodeConnectedNodeError


class TestNode():
    def test_add_node(self):
        node = Node("test", "type_test", (1, 1), "zone_test")
        node2 = Node("test2", "type_test2", (1, 2), "zone_test")
        node3 = Node("test3", "type_test3", (1, 3), "zone_test")

        node.add_connected_node(node2)
        node.add_connected_node(node3)

        assert node2 in node.connected_nodes
        assert node3 in node.connected_nodes

    def test_add_same_node(self):
        try:
            node = Node("test", "type_test", (1, 1), "zone_test")
            node.add_connected_node(node)
            pytest.fail("INVALID[ Add same Node ]")
        except NodeConnectedNodeError:
            pass

    def test_add_again_node(self):
        try:
            node = Node("test", "type_test", (1, 1), "zone_test")
            node3 = Node("test3", "type_test3", (1, 3), "zone_test")
            node.add_connected_node(node3)
            node.add_connected_node(node3)
            pytest.fail("INVALID[ Add a Node again ]")
        except NodeConnectedNodeError:
            pass
