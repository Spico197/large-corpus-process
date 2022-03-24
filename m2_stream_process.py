import time
from typing import Iterator


def pick_one_student(dorm: str) -> Iterator[str]:
    with open(dorm, "rt", encoding="utf8") as fin:
        for student in fin:
            yield student


def pick_sample(student: str) -> str:
    time.sleep(0.01)
    sample = f"{student.strip()}'s sample"
    return sample


def process(dorm: str, sample_storeroom: str) -> None:
    with open(sample_storeroom, "wt", encoding="utf8") as fout:
        for student in pick_one_student(dorm):
            sample = pick_sample(student)
            fout.write(f"{sample}\n")
            fout.flush()


if __name__ == "__main__":
    process(
        "student_names.txt",
        "sample_storeroom.txt"
    )
