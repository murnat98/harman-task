from dataclasses import dataclass

from task_queue.structures.resources import Resources


@dataclass
class Task:
    id: int
    priority: int
    resources: Resources
    content: str
    result: str
