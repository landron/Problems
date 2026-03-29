# ruff & black
import unittest


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def create_linked_list(values):
    head = None
    tail = None
    for value in values:
        node = Node(value)
        if head is None:
            head = node
            tail = node
        else:
            tail.next = node
            tail = node
    return head


def kth_to_last(head, k):
    if k <= 0:
        return None

    first = head
    second = head

    for _ in range(k):
        if second is None:
            return None
        second = second.next

    while second is not None:
        first = first.next
        second = second.next

    return first


class TestKthToLast(unittest.TestCase):
    def test_k_greater_than_length(self):
        head = create_linked_list([1, 2, 3])
        node = kth_to_last(head, 4)
        self.assertIsNone(node)

    def test_empty_list(self):
        head = None
        node = kth_to_last(head, 1)
        self.assertIsNone(node)

    def test_single_node(self):
        head = create_linked_list([55])
        node = kth_to_last(head, 1)
        self.assertIsNotNone(node)
        self.assertEqual(node.data, 55)

    def test_overloads_const_and_non_const(self):
        head = create_linked_list([1, 2, 3, 4, 5])

        mutable_result = kth_to_last(head, 2)
        self.assertIsNotNone(mutable_result)
        self.assertEqual(mutable_result.data, 4)

        const_head = head
        const_result = kth_to_last(const_head, 2)
        self.assertIsNotNone(const_result)
        self.assertEqual(const_result.data, 4)

    def test_boundaries(self):
        head = create_linked_list([10, 20, 30, 40])

        tail = kth_to_last(head, 1)
        self.assertIsNotNone(tail)
        self.assertEqual(tail.data, 40)

        first = kth_to_last(head, 4)
        self.assertIsNotNone(first)
        self.assertEqual(first.data, 10)

    def test_sample(self):
        head = create_linked_list([1, 2, 3, 4, 5])
        node = kth_to_last(head, 2)
        self.assertIsNotNone(node)
        self.assertEqual(node.data, 4)


if __name__ == "__main__":
    unittest.main()
