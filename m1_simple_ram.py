import time
from typing import List


def pick_all_students(dorm: str) -> List[str]:
    with open(dorm, "rt", encoding="utf8") as fin:
        students = fin.readlines()
        return students


def pick_sample(student: str) -> str:
    time.sleep(0.01)
    sample = f"{student.strip()}'s sample"
    return sample


def process(dorm: str, sample_storeroom: str) -> None:
    with open(sample_storeroom, "wt", encoding="utf8") as fout:
        students = pick_all_students(dorm)
        for student in students:
            sample = pick_sample(student)
            fout.write(f"{sample}\n")
            fout.flush()


if __name__ == "__main__":
    process(
        "student_names.txt",
        "sample_storeroom.txt"
    )
