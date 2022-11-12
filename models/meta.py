from dataclasses import dataclass


@dataclass
class Meta:
    name: str
    description: str
    version: str

    def __str__(self) -> str:
        return f'{self.name} {self.version}'