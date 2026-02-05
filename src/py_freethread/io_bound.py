#!/usr/bin/env python3
"""
I/O-Bound Workload Example

Demonstrates threading behavior for I/O-bound tasks.
Even with the GIL, I/O-bound tasks benefit from threading because
the GIL is released during I/O operations.
"""

import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor


def main():
    print("Python Free-Threading Demo: I/O-Bound Workload")
    print("=" * 50)

    # Check GIL status
    gil_enabled = sys._is_gil_enabled()
    print(f"\nGIL enabled: {gil_enabled}")
    print(f"Python version: {sys.version}")

    # Define I/O-bound tasks (simulated I/O delays in seconds)
    tasks = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]  # Eight 0.5s I/O operations
    num_workers = 4

    print(f"\nRunning {len(tasks)} I/O tasks (0.5s each)")

    # Run sequential baseline
    sequential_time = run_sequential(tasks)

    # Run threaded version
    threaded_time = run_threaded(tasks, num_workers)

    # Calculate speedup
    speedup = sequential_time / threaded_time

    print("\n" + "=" * 50)
    print("Results:")
    print(f"  Sequential: {sequential_time:.3f}s")
    print(f"  Threaded:   {threaded_time:.3f}s")
    print(f"  Speedup:    {speedup:.2f}x")

    print("\n💡 I/O-bound tasks benefit from threading REGARDLESS of GIL status")
    print("   because the GIL is released during I/O operations.")

    if not gil_enabled:
        print("\n   With GIL disabled, there may be slight overhead differences,")
        print("   but the main benefit comes from concurrent I/O, not CPU parallelism.")


def run_sequential(tasks: list[float]) -> float:
    """Run I/O tasks sequentially."""
    print("\n=== Sequential Execution ===")
    start = time.perf_counter()

    for i, duration in enumerate(tasks):
        task_id, elapsed = simulate_io_operation(i, duration)
        print(f"Task {task_id}: completed in {elapsed:.3f}s")

    total_time = time.perf_counter() - start
    print(f"Total time: {total_time:.3f}s")
    return total_time


def run_threaded(tasks: list[float], num_workers: int) -> float:
    """Run I/O tasks using a thread pool."""
    print(f"\n=== Threaded Execution ({num_workers} workers) ===")
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(simulate_io_operation, i, duration)
            for i, duration in enumerate(tasks)
        ]

        for future in futures:
            task_id, elapsed = future.result()
            print(f"Task {task_id}: completed in {elapsed:.3f}s")

    total_time = time.perf_counter() - start
    print(f"Total time: {total_time:.3f}s")
    return total_time


def simulate_io_operation(task_id: int, duration: float) -> tuple[int, float]:
    """Simulate an I/O-bound operation (e.g., network request, file I/O)."""
    start = time.perf_counter()
    time.sleep(duration)  # Simulates I/O wait (GIL is released during sleep)
    elapsed = time.perf_counter() - start
    return task_id, elapsed


if __name__ == "__main__":
    main()
