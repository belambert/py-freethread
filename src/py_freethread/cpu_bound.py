#!/usr/bin/env python3
"""
CPU-Bound Workload Example

Demonstrates the performance difference between threaded execution
with and without the GIL for CPU-intensive tasks.
"""

import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor


def main():
    print("Python Free-Threading Demo: CPU-Bound Workload")
    print("=" * 50)

    # Check GIL status
    gil_enabled = sys._is_gil_enabled()
    print(f"\nGIL enabled: {gil_enabled}")
    print(f"Python version: {sys.version}")

    # Define CPU-intensive tasks (adjust n based on your system)
    tasks = [35, 35, 35, 35]  # Four Fibonacci calculations
    num_workers = 4

    print(f"\nRunning {len(tasks)} tasks: {tasks}")

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

    if gil_enabled:
        print("\n⚠️  GIL is ENABLED - threads cannot execute CPU-bound code in parallel")
        print("   Speedup is limited by the GIL")
    else:
        print("\n✓  GIL is DISABLED - threads can execute in parallel!")
        print(f"   Achieved {speedup:.2f}x speedup with {num_workers} workers")


def run_sequential(tasks: list[int]) -> float:
    """Run tasks sequentially."""
    print("\n=== Sequential Execution ===")
    start = time.perf_counter()

    for i, n in enumerate(tasks):
        task_id, result, duration = cpu_intensive_task(i, n)
        print(f"Task {task_id}: fib({n}) = {result} (took {duration:.3f}s)")

    total_time = time.perf_counter() - start
    print(f"Total time: {total_time:.3f}s")
    return total_time


def run_threaded(tasks: list[int], num_workers: int) -> float:
    """Run tasks using a thread pool."""
    print(f"\n=== Threaded Execution ({num_workers} workers) ===")
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(cpu_intensive_task, i, n) for i, n in enumerate(tasks)]

        for future in futures:
            task_id, result, duration = future.result()
            print(f"Task {task_id}: fib({tasks[task_id]}) = {result} (took {duration:.3f}s)")

    total_time = time.perf_counter() - start
    print(f"Total time: {total_time:.3f}s")
    return total_time


def cpu_intensive_task(task_id: int, n: int) -> tuple[int, int, float]:
    """Run a CPU-intensive task and return timing information."""
    start = time.perf_counter()
    result = fibonacci(n)
    duration = time.perf_counter() - start
    return task_id, result, duration


def fibonacci(n: int) -> int:
    """Compute the nth Fibonacci number (CPU-intensive)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == "__main__":
    main()
