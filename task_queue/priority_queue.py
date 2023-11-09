import logging
from typing import Callable, Optional, Self

from task_queue.errors import IncorrectNodeError
from task_queue.settings import Settings

logger = logging.getLogger(__name__)


class PriorityNode[T]:
    """
    A node in a linked list
    """

    def __init__(
        self,
        next_item: Optional[Self],
        prev_item: Optional[Self],
        priority: int,
        item: T,
    ):
        self.next_item = next_item
        self.prev_item = prev_item
        self.priority = priority
        self.item = item


def dump(func: Callable):
    def wrapper(self, *args, **kwargs):
        if Settings.DEBUG:
            self._dump(f"{func.__name__} START")

        result = func(self, *args, **kwargs)

        if Settings.DEBUG:
            self._dump(f"{func.__name__} END")
        return result

    return wrapper


class PriorityQueue[T]:
    """
    A priority queue implemented as a sorted linked list
    """

    def __init__(self):
        self._head: Optional[PriorityNode[T]] = None
        self._length = 0

    @dump
    def insert(self, priority: int, item: T):
        inserted = False
        node = self._head

        for node in self:
            if priority > node.priority:
                inserted = True
                new_node = PriorityNode(node, node.prev_item, priority, item)

                if node.prev_item is not None:
                    node.prev_item.next_item = new_node
                else:
                    self._head = new_node

                node.prev_item = new_node

                break

        if not inserted:
            new_node = PriorityNode(None, node, priority, item)
            if node is not None:
                node.next_item = new_node
            else:
                self._head = new_node

        self._length += 1

    @dump
    def pop(self) -> Optional[T]:
        if self._head is None:
            return None

        item = self._head.item
        self._head = self._head.next_item
        if self._head is not None:
            self._head.prev_item = None
        self._length -= 1

        return item

    @dump
    def remove(self, node: PriorityNode[T]):
        if node.prev_item is not None:
            node.prev_item.next_item = node.next_item
        else:
            if node is self._head:
                self._head = node.next_item
            else:
                raise IncorrectNodeError("Node is not in the queue")

        if node.next_item is not None:
            node.next_item.prev_item = node.prev_item

        self._length -= 1

    @dump
    def peek(self) -> Optional[T]:
        if self._head is None:
            return None

        return self._head.item

    def _dump(self, operation: str = None, is_start: bool = True):
        logger.debug("========= QUEUE DUMP =========")
        logger.debug(f"Operation: {operation} {'START' if is_start else 'END'}")
        logger.debug(f"Size: {self._length}")
        for node in self:
            next_node = id(node.next_item) if node.next_item is not None else None
            prev_node = id(node.prev_item) if node.prev_item is not None else None
            logger.debug(
                f"Node[{id(node)}] - Priority: {node.priority}, Item: {node.item}, "
                f"Next: {next_node}, Prev: {prev_node}"
            )

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Self:
        self._current_node = self._head
        return self

    def __next__(self) -> PriorityNode[T]:
        if self._current_node is None:
            raise StopIteration

        node = self._current_node
        self._current_node = self._current_node.next_item
        return node
