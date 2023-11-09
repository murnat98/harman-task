from typing import Optional
from task_queue.priority_queue import PriorityQueue
from task_queue.structures.resources import Resources
from task_queue.structures.task import Task


class TaskQueue:
    def __init__(self):
        self._queue = PriorityQueue[Task]()

    def add_task(self, task: Task):
        self._queue.insert(task.priority, task)

    def get_task(self, available_resources: Resources) -> Optional[Task]:
        for node in self._queue:
            task = node.item
            if task.resources.satisfies_resources(available_resources):
                self._queue.remove(node)
                return task

        return None
