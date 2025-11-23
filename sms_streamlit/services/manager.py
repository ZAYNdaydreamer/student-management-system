import json
import os
from typing import List, Optional, Dict, Any
from models.student import Student

class StudentManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump([], f)

    def _read_all(self) -> List[Dict[str, Any]]:
        with open(self.filepath, "r") as f:
            return json.load(f)

    def _write_all(self, data: List[Dict[str, Any]]):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def list_students(self) -> List[Student]:
        rows = self._read_all()
        return [Student(**r) for r in rows]

    def add_student(self, data: Dict[str, Any]) -> Student:
        rows = self._read_all()
        next_id = max([r.get("id", 0) for r in rows], default=0) + 1
        data["id"] = next_id
        student = Student(**data)
        rows.append(student.to_dict())
        self._write_all(rows)
        return student

    def get_student(self, student_id: int) -> Optional[Student]:
        rows = self._read_all()
        for r in rows:
            if int(r.get("id")) == int(student_id):
                return Student(**r)
        return None

    def update_student(self, student_id: int, updates: Dict[str, Any]) -> Optional[Student]:
        rows = self._read_all()
        for idx, r in enumerate(rows):
            if int(r.get("id")) == int(student_id):
                r.update(updates)
                rows[idx] = r
                self._write_all(rows)
                return Student(**r)
        return None

    def delete_student(self, student_id: int) -> bool:
        rows = self._read_all()
        new = [r for r in rows if int(r.get("id")) != int(student_id)]
        if len(new) == len(rows):
            return False
        self._write_all(new)
        return True

    def search(self, q: str = "", grade: str = "", min_age: int = None, max_age: int = None,
               min_gpa: float = None, max_gpa: float = None) -> List[Student]:
        rows = self._read_all()
        results = []
        q_lower = q.lower().strip()
        for r in rows:
            match = True
            if q_lower:
                match = q_lower in r.get("name","").lower() or q_lower in str(r.get("id",""))
            if match and grade:
                match = r.get("grade","").lower() == grade.lower()
            if match and min_age is not None:
                match = int(r.get("age",0)) >= int(min_age)
            if match and max_age is not None:
                match = int(r.get("age",0)) <= int(max_age)
            if match and min_gpa is not None:
                match = float(r.get("gpa",0.0)) >= float(min_gpa)
            if match and max_gpa is not None:
                match = float(r.get("gpa",0.0)) <= float(max_gpa)
            if match:
                results.append(Student(**r))
        return results