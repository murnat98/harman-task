from dataclasses import dataclass
from typing import Self


@dataclass
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int

    def satisfies_resources(self, resources: Self) -> bool:
        return (
            resources.ram >= self.ram
            and resources.cpu_cores >= self.cpu_cores
            and resources.gpu_count >= self.gpu_count
        )
