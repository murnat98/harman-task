import enum
from unittest import TestCase
from task_queue.logging_configuration import init_logger
from task_queue.structures.resources import Resources
from task_queue.structures.task import Task

from task_queue.task_queue import TaskQueue


class TestTaskQueue(TestCase):
    class _LimitTypes(enum.Enum):
        CPU = enum.auto()
        RAM = enum.auto()
        GPU = enum.auto()

    _RESOURCE_LIMITS_MAPPING = {
        _LimitTypes.RAM: [
            Resources(1, 0, 0),
            Resources(2, 0, 0),
            Resources(3, 0, 0),
            Resources(4, 0, 0),
        ],
        _LimitTypes.CPU: [
            Resources(0, 1, 0),
            Resources(0, 2, 0),
            Resources(0, 3, 0),
            Resources(0, 4, 0),
        ],
        _LimitTypes.GPU: [
            Resources(0, 0, 1),
            Resources(0, 0, 2),
            Resources(0, 0, 3),
            Resources(0, 0, 4),
        ],
    }

    _RESOURCE_LIMITS_TEST_CHECK_MAPPING = {
        _LimitTypes.RAM: [
            Resources(0, 0, 0),
            Resources(10, 0, 0),
            Resources(1, 0, 0),
            Resources(3, 0, 0),
        ],
        _LimitTypes.CPU: [
            Resources(0, 0, 0),
            Resources(0, 10, 0),
            Resources(0, 1, 0),
            Resources(0, 3, 0),
        ],
        _LimitTypes.GPU: [
            Resources(0, 0, 0),
            Resources(0, 0, 10),
            Resources(0, 0, 1),
            Resources(0, 0, 3),
        ],
    }

    def setUp(self):
        init_logger("DEBUG")

    def test_empty(self):
        queue = TaskQueue()

        task = queue.get_task(Resources(100, 100, 100))
        self.assertIsNone(task)

    def test_order(self):
        queue = TaskQueue()

        resource_10 = Resources(4, 4, 2)
        resource_5 = Resources(8, 1, 3)
        resource_11 = Resources(2, 2, 1)
        resource_3 = Resources(1, 1, 8)

        task_10 = Task(1, 10, resource_10, "task1", "task1")
        task_5 = Task(2, 5, resource_5, "task2", "task2")
        task_11 = Task(3, 11, resource_11, "task3", "task3")
        task_3 = Task(4, 3, resource_3, "task4", "task4")

        queue.add_task(task_10)
        queue.add_task(task_5)
        queue.add_task(task_11)
        queue.add_task(task_3)

        task = queue.get_task(Resources(0, 0, 0))
        self.assertIsNone(task)

        task = queue.get_task(Resources(2, 2, 1))
        self.assertEqual(task, task_11)

        task = queue.get_task(Resources(1, 1, 8))
        self.assertEqual(task, task_3)

        task = queue.get_task(Resources(10, 10, 8))
        self.assertEqual(task, task_10)

        task = queue.get_task(Resources(10, 10, 8))
        self.assertEqual(task, task_5)

    def _test_specific_limits(self, limit_type: _LimitTypes):
        queue = TaskQueue()
        resources = self._RESOURCE_LIMITS_MAPPING[limit_type]

        task_1 = Task(1, 1, resources[0], "task1", "task1")
        task_2 = Task(2, 2, resources[2], "task2", "task2")
        task_3 = Task(3, 3, resources[1], "task3", "task3")
        task_4 = Task(4, 4, resources[3], "task4", "task4")

        queue.add_task(task_3)
        queue.add_task(task_1)
        queue.add_task(task_4)
        queue.add_task(task_2)

        test_check_resources = self._RESOURCE_LIMITS_TEST_CHECK_MAPPING[limit_type]

        self.assertIsNone(queue.get_task(test_check_resources[0]))
        self.assertEqual(queue.get_task(test_check_resources[1]), task_4)
        self.assertEqual(queue.get_task(test_check_resources[2]), task_1)
        self.assertIsNone(queue.get_task(test_check_resources[2]))
        self.assertEqual(queue.get_task(test_check_resources[3]), task_3)
        self.assertEqual(queue.get_task(test_check_resources[3]), task_2)
        self.assertIsNone(queue.get_task(test_check_resources[1]))

    def test_ram_limits(self):
        self._test_specific_limits(self._LimitTypes.RAM)

    def test_cpu_limits(self):
        self._test_specific_limits(self._LimitTypes.CPU)

    def test_gpu_limits(self):
        self._test_specific_limits(self._LimitTypes.GPU)
