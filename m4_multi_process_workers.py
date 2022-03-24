import time
from multiprocessing import Queue, Process, cpu_count
from typing import Iterator


def pick_student(stu_queue: Queue, dorm: str, num_workers: int) -> Iterator[str]:
    print("pick_student: started")

    picked_num = 0
    with open(dorm, "rt", encoding="utf8") as fin:
        for student in fin:
            stu_queue.put(student)
            picked_num += 1
            if picked_num % 500 == 0:
                print(f"pick_student: {picked_num}")

    # end signal
    for _ in range(num_workers):
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
    num_process = max(1, cpu_count() - 1)

    maxsize = 10 * num_process
    stu_queue = Queue(maxsize=maxsize)
    store_queue = Queue(maxsize=maxsize)

    store_p = Process(target=store_sample, args=(store_queue, sample_storeroom), daemon=True)
    store_p.start()
    process_workers = []
    for _ in range(num_process):
        process_p = Process(target=process, args=(stu_queue, store_queue), daemon=True)
        process_p.start()
        process_workers.append(process_p)
    read_p = Process(target=pick_student, args=(stu_queue, dorm, num_process), daemon=True)
    read_p.start()

    for worker in process_workers:
        worker.join()

    # end signal
    store_queue.put(None)
    store_p.join()
