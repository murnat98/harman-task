from task_queue.command_processor import TaskQueueCommandProcessor
from task_queue.task_queue import TaskQueue


def main():
    task_queue = TaskQueue()
    task_queue_command_processor = TaskQueueCommandProcessor(task_queue)
    task_queue_command_processor.run()


if __name__ == "__main__":
    main()
