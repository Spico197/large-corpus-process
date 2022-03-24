import time
from multiprocessing import Queue, Process
from typing import Iterator


def pick_student(stu_queue: Queue, dorm: str) -> Iterator[str]:
    print("pick_student: started")

    picked_num = 0
    with open(dorm, "rt", encoding="utf8") as fin:
        for student in fin:
            stu_queue.put(student)
            picked_num += 1
            if picked_num % 500 == 0:
                print(f"pick_student: {picked_num}")

    # end signal
    stu_queue.put(None)
    print("pick_student: finished")


def pick_sample(student: str) -> str:
    time.sleep(0.01)
    sample = f"{student.strip()}'s sample"
    return sample


def process(stu_queue: Queue, store_queue: Queue) -> None:
    print("process: started")

    process_num = 0
    while True:
        student = stu_queue.get()
        if student is not None:
            sample = pick_sample(student)
            store_queue.put(sample)
            process_num += 1
            if process_num % 500 == 0:
                print(f"process: {process_num}")
        else:
            break

    # end signal
    store_queue.put(None)
    print("process: finished")


def store_sample(store_queue: Queue, sample_storeroom: str) -> None:
    print("store_sample: started")

    store_num = 0
    with open(sample_storeroom, "wt", encoding="utf8") as fout:
        while True:
            sample = store_queue.get()
            if sample is not None:
                fout.write(f"{sample}\n")
                fout.flush()

                store_num += 1
                if store_num % 500 == 0:
                    print(f"store_sample: {store_num}")
            else:
                break

    print("store_sample: finished")


if __name__ == "__main__":
    dorm = "student_names.txt"
    sample_storeroom = "sample_storeroom.txt"

    stu_queue = Queue()
    store_queue = Queue()

    store_p = Process(target=store_sample, args=(store_queue, sample_storeroom), daemon=True)
    store_p.start()
    process_p = Process(target=process, args=(stu_queue, store_queue), daemon=True)
    process_p.start()
    read_p = Process(target=pick_student, args=(stu_queue, dorm), daemon=True)
    read_p.start()

    store_p.join()
