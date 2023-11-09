# Task Queue

A task queue with priorities and resource limits

## Dependencies

- [Python 3.12](https://www.python.org/downloads/release/python-3120/)
- [Poetry](https://python-poetry.org/docs/)

## Installation

```bash
poetry install
```

## Run

To run the tests
```bash
poetry run python -m unittest discover tests
```

To run the CLI and add manually the tasks
```bash
poetry run python -m task_queue
```

For manual of the inner commands run `help`

## Solution

Some comments on the solution architecture decision and future comments:

- Decided to create an in-memory storage according to what requirements we had
- A sorted doubly linked list data structure is choosen for the storage of tasks, so we get O(n) on insert and O(1) on get
- For further development there is a good idea to store that storage in a mongo db for example and listen for requests
