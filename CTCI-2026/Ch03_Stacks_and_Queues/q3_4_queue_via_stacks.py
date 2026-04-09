"""Queue from Two Stacks
https://www.hackerrank.com/contests/software-engineer-prep-kit/challenges/queue-from-two-stacks

To achieve amortized O(1), you must keep the elements in the second stack until they
are actually needed or the stack is empty.

Complexity: O(1) amortized Time (all operations) | O(n) Space
Tags: #queue #stack #amortized
Compliance: ruff & pylint clean.
"""

import sys
import unittest


class Queue:
    """Queue implemented using two stacks."""

    def __init__(self):
        # We use Python lists as the underlying Data Structure
        # to implement the Stack behavior.
        self.stack_in = []
        self.stack_out = []

        # We track size manually to remain implementation-agnostic.
        # This ensures the Queue behavior is consistent even if
        # the underlying stacks didn't support a len() operation.
        self.size = 0

    def enqueue(self, value):
        """Add an element to the end of the queue."""
        self.stack_in.append(value)
        self.size += 1

    def dequeue(self):
        """Remove and return the element at the front of the queue."""
        if self.empty():
            raise IndexError("Dequeue from an empty queue")
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
        value = self.stack_out.pop()
        self.size -= 1
        return value

    def __len__(self):
        """Return the number of elements in the queue."""
        return self.size

    def empty(self):
        """Check if the queue is empty."""
        return self.size == 0

    def peek(self):
        """Return the element at the front of the queue without removing it."""
        if self.empty():
            raise IndexError("Peek from an empty queue")
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
        return self.stack_out[-1]


def process(operations, values):
    """Process a list of queue operations and return the results."""
    if not operations:
        return []

    queue = Queue()
    ret = []

    dispatch = {
        "enqueue": queue.enqueue,
        "dequeue": lambda v: ret.append(queue.dequeue()),
        "size": lambda v: ret.append(len(queue)),
        "peek": lambda v: ret.append(queue.peek()),
    }

    for i, op in enumerate(operations):
        op = op.strip().lower()
        # values.pop(0) is an O(N) operation
        value = values[i]
        dispatch[op](value)

    return ret


class TestProcessFunction(unittest.TestCase):
    """Unit tests for the process function."""

    def test_empty_operations(self):
        """Test with no operations."""
        result = process([], [])
        self.assertEqual(result, [])

    def test_single_enqueue(self):
        """Test single enqueue operation."""
        result = process(["enqueue"], [5])
        self.assertEqual(result, [])

    def test_enqueue_dequeue(self):
        """Test enqueue followed by dequeue."""
        result = process(["enqueue", "dequeue"], [10, None])
        self.assertEqual(result, [10])

    def test_size_operation(self):
        """Test size operation."""
        result = process(["enqueue", "enqueue", "size"], [1, 2, None])
        self.assertEqual(result, [2])

    def test_peek_operation(self):
        """Test peek operation."""
        result = process(["enqueue", "enqueue", "peek"], [7, 8, None])
        self.assertEqual(result, [7])

    def test_complex_sequence(self):
        """Test a complex sequence of operations."""
        operations = [
            "enqueue",
            "enqueue",
            "enqueue",
            "dequeue",
            "dequeue",
            "enqueue",
            "peek",
            "size",
            "dequeue",
        ]
        values = [1, 2, 3, None, None, 4, None, None, None]

        result = process(operations, values)
        # First dequeue: 1, Second dequeue: 2
        # Peek (at 3): 3, Size: 2 (3 and 4), Last dequeue: 3
        self.assertEqual(result, [1, 2, 3, 2, 3])

    def test_case_insensitive_operations(self):
        """Test that operations are case-insensitive."""
        result = process(
            ["ENQUEUE", "ENQUEUE", "Dequeue", "PEEK"],
            [42, 99, None, None],
        )
        self.assertEqual(result[0], 42)  # First dequeue result
        self.assertEqual(result[1], 99)  # Peek result


def main():
    """main"""


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "main":
        main()
    else:
        unittest.main()
