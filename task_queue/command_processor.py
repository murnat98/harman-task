import argparse
import shlex
from task_queue.structures.resources import Resources
from task_queue.structures.task import Task
from task_queue.task_queue import TaskQueue


class TaskQueueCommandProcessor:
    _COMMAND_PROCESSOR_MAPPING = {
        "add": "_add_task",
        "get": "_get_task",
        "help": "_help_command",
    }
    _ARGUMENT_PARSER_MAPPING = {
        "add": "_parse_add_arguments",
        "get": "_parse_get_arguments",
        "help": "_parse_help_arguments",
    }

    def __init__(self, task_queue: TaskQueue):
        self.task_queue = task_queue

    def process_command(self, command: str) -> str:
        command_parts = shlex.split(command)
        if len(command_parts) == 0:
            return ""

        command_name = command_parts[0]
        command_args = command_parts[1:]

        try:
            parsed_args = self._parse_arguments(command_name, command_args)
        except SystemExit:
            return ""

        try:
            command_method = getattr(
                self, self._COMMAND_PROCESSOR_MAPPING[command_name]
            )
        except KeyError:
            raise ValueError(f"Unknown command: {command_name}")
        else:
            return command_method(parsed_args)

    def _parse_add_arguments(self, command_args: list[str]) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog="add")
        parser.add_argument("-i", "--id", type=int, required=True, help="Task ID")
        parser.add_argument(
            "-p", "--priority", type=int, required=True, help="Priority"
        )
        parser.add_argument(
            "-c", "--cpu", type=int, required=True, help="Required CPU cores"
        )
        parser.add_argument(
            "-g", "--gpu", type=int, required=True, help="Required GPU cores"
        )
        parser.add_argument("-r", "--ram", type=int, required=True, help="Required RAM")
        parser.add_argument(
            "-C", "--content", type=str, required=True, help="Task content"
        )
        parser.add_argument(
            "-R", "--result", type=str, required=True, help="Task result"
        )

        return parser.parse_args(command_args)

    def _parse_get_arguments(self, command_args: list[str]) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog="get")
        parser.add_argument(
            "-c", "--cpu", type=int, required=True, help="Available CPU cores"
        )
        parser.add_argument(
            "-g", "--gpu", type=int, required=True, help="Available GPU cores"
        )
        parser.add_argument(
            "-r", "--ram", type=int, required=True, help="Available RAM"
        )

        return parser.parse_args(command_args)

    def _parse_help_arguments(self, command_args: list[str]) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog="help")

        return parser.parse_args(command_args)

    def _help_command(self, args: argparse.ArgumentParser) -> str:
        return (
            "Available commands:\n"
            "add Add a new task\n"
            "get Get a task\n"
            "help Print this help message\n"
        )

    def _add_task(self, args: argparse.ArgumentParser) -> str:
        self.task_queue.add_task(
            Task(
                id=args.id,
                priority=args.priority,
                resources=Resources(
                    cpu_cores=args.cpu, gpu_count=args.gpu, ram=args.ram
                ),
                content=args.content,
                result=args.result,
            )
        )

        return "Task added"

    def _get_task(self, args: argparse.ArgumentParser) -> str:
        task = self.task_queue.get_task(
            Resources(cpu_cores=args.cpu, gpu_count=args.gpu, ram=args.ram)
        )
        if task is None:
            return "No task available"
        else:
            return f"Task {task} retrieved"

    def _parse_arguments(
        self, command_name: str, command_args: list[str]
    ) -> argparse.ArgumentParser:
        try:
            parser_method = getattr(self, self._ARGUMENT_PARSER_MAPPING[command_name])
        except KeyError:
            raise ValueError(f"Unable to parse arguments for command: {command_name}")
        else:
            return parser_method(command_args)

    def run(self):
        while True:
            try:
                command = input("> ")
            except KeyboardInterrupt:
                print()
                continue
            except EOFError:
                break

            try:
                result = self.process_command(command)
            except Exception as e:
                print(f"Error: {e}")
            else:
                if result:
                    print(result)
