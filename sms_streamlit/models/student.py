from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Student:
    id: int
    name: str
    age: int
    grade: str
    email: Optional[str] = None
    gpa: float = 0.0
    notes: Optional[str] = None

    def to_dict(self):
        return asdict(self)