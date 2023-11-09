import unittest
from task_queue.logging_configuration import init_logger
from task_queue.errors import IncorrectNodeError

from task_queue.priority_queue import PriorityQueue


class TestPriorityQueue(unittest.TestCase):
    def setUp(self):
        init_logger("DEBUG")

    def test_empty(self):
        queue = PriorityQueue[int]()

        head_value = queue.pop()
        self.assertIsNone(head_value)

        head_value = queue.peek()
        self.assertIsNone(head_value)

    def test_len(self):
        queue = PriorityQueue[int]()
        self.assertEqual(len(queue), 0)

        queue.insert(0, 0)
        self.assertEqual(len(queue), 1)

        queue.insert(1, 1)
        self.assertEqual(len(queue), 2)

        queue.pop()
        self.assertEqual(len(queue), 1)

        queue.insert(2, 2)
        self.assertEqual(len(queue), 2)

        queue.insert(3, 3)
        self.assertEqual(len(queue), 3)

        queue.pop()
        self.assertEqual(len(queue), 2)

        queue.pop()
        self.assertEqual(len(queue), 1)

        pop = queue.pop()
        self.assertEqual(len(queue), 0)

        pop = queue.pop()
        self.assertEqual(len(queue), 0)
        self.assertIsNone(pop)

    def test_order(self):
        queue = PriorityQueue[int]()
        queue.insert(1, 1)
        queue.insert(0, 0)
        queue.insert(2, 2)

        self.assertEqual(queue.pop(), 2)
        self.assertEqual(queue.pop(), 1)
        self.assertEqual(queue.pop(), 0)

        queue = PriorityQueue[int]()
        queue.insert(2, 2)
        queue.insert(3, 3)
        queue.insert(1, 1)
        queue.insert(4, 4)
        queue.insert(5, 5)
        queue.insert(6, 6)

        self.assertEqual(queue.pop(), 6)
        self.assertEqual(queue.pop(), 5)
        self.assertEqual(queue.pop(), 4)
        self.assertEqual(queue.pop(), 3)
        self.assertEqual(queue.pop(), 2)
        self.assertEqual(queue.pop(), 1)

        queue = PriorityQueue[int]()
        queue.insert(6, 6)
        queue.insert(2, 2)
        queue.insert(4, 4)
        queue.insert(-3, -3)
        queue.insert(1, 1)
        queue.insert(5, 5)

        self.assertEqual(queue.pop(), 6)
        self.assertEqual(queue.pop(), 5)
        self.assertEqual(queue.pop(), 4)
        self.assertEqual(queue.pop(), 2)
        self.assertEqual(queue.pop(), 1)
        self.assertEqual(queue.pop(), -3)

    def test_peek(self):
        queue = PriorityQueue[int]()
        queue.insert(1, 1)
        queue.insert(0, 0)
        queue.insert(2, 2)

        self.assertEqual(queue.peek(), 2)
        self.assertEqual(queue.peek(), 2)

    def test_remove(self):
        queue = PriorityQueue[int]()
        queue.insert(1, 1)
        queue.insert(0, 0)
        queue.insert(2, 2)

        initial_head = queue._head

        queue.remove(queue._head.next_item)
        self.assertEqual(queue.pop(), 2)
        self.assertEqual(queue.pop(), 0)

        queue.insert(1, 1)
        queue.insert(0, 0)
        queue.insert(2, 2)

        queue.remove(queue._head)
        self.assertEqual(queue.pop(), 1)
        self.assertEqual(queue.pop(), 0)

        queue.insert(1, 1)
        queue.insert(2, 2)
        queue.insert(0, 0)

        self.assertRaises(IncorrectNodeError, queue.remove, initial_head)
