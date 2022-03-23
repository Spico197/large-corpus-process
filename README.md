# large-corpus-process

Tutorial for simple methods to process corpora.

## Methods

1. Read all content from file to memory, and dump the results after processed.
2. Process and dump while reading streamly.
3. Split reading, processing and dumping into 3 processes.
4. method 3 w/ multiple processing workers.

## Benchmark

| Method                        |      Time |
| :---------------------------- | --------: |
| 1                             | 1m40.716s |
| 2                             | 1m40.717s |
| 2 w/ 10 ms reading time delay | 3m21.345s |
| 3                             | 1m41.097s |
| 4                             |  0m4.160s |
