#!/usr/bin/env python3
"""
GIL Control and Monitoring

Demonstrates how to check GIL status and provides utilities for monitoring
threading behavior.
"""

import sys
import threading
import time
from typing import Optional


def main():
    """Main entry point - shows GIL status and monitors thread parallelism."""
    print_gil_info()

    # Monitor execution patterns
    monitor_thread_execution(cpu_intensive_work, duration=1.0)

    print("\n" + "=" * 50)
    print("Tips:")
    print("  - Use sys._is_gil_enabled() to check GIL status")
    print("  - With GIL disabled, always use locks for shared data")
    print("  - Profile your code to measure actual parallelism")
    print("  - Not all workloads benefit from free-threading")


def print_gil_info():
    """Print detailed GIL information."""
    print("Python GIL Status")
    print("=" * 50)

    info = check_gil_status()

    print(f"\nPython Version: {info['python_version']}")
    print(f"GIL Enabled: {info['gil_enabled']}")
    print(f"Current Thread: {info['thread_info']}")

    if info["gil_enabled"]:
        print("\n⚠️  Running with GIL ENABLED")
        print("   - Thread safety: Many operations are implicitly atomic")
        print("   - CPU parallelism: Limited to one thread executing Python at a time")
        print("   - I/O parallelism: Works well (GIL released during I/O)")
    else:
        print("\n✓  Running with GIL DISABLED (free-threading)")
        print("   - Thread safety: Explicit synchronization required!")
        print("   - CPU parallelism: True parallel execution possible")
        print("   - I/O parallelism: Works well")
        print("\n   ⚠️  IMPORTANT: You must use locks for shared mutable state!")


def monitor_thread_execution(func, *args, duration: float = 1.0):
    """
    Monitor thread execution patterns.

    This helps visualize whether threads are truly running in parallel.
    """
    print(f"\n\nMonitoring thread execution for {duration}s...")
    print("=" * 50)

    results = []
    lock = threading.Lock()

    def worker(thread_id: int):
        start = time.perf_counter()
        iterations = 0

        while time.perf_counter() - start < duration:
            func(*args)
            iterations += 1

        elapsed = time.perf_counter() - start

        with lock:
            results.append(
                {
                    "thread_id": thread_id,
                    "iterations": iterations,
                    "time": elapsed,
                    "throughput": iterations / elapsed,
                }
            )

    num_threads = 4
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(num_threads)]

    start_time = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    total_time = time.perf_counter() - start_time

    # Print results
    print("\nPer-Thread Results:")
    total_iterations = 0
    for r in results:
        print(
            f"  Thread {r['thread_id']}: "
            f"{r['iterations']:,} iterations, "
            f"{r['throughput']:.0f} iter/sec"
        )
        total_iterations += r["iterations"]

    overall_throughput = total_iterations / total_time
    print(f"\nOverall: {total_iterations:,} iterations, " f"{overall_throughput:.0f} iter/sec")

    # Analyze parallelism
    expected_parallel_throughput = results[0]["throughput"] * num_threads
    parallelism_ratio = overall_throughput / results[0]["throughput"]

    print(f"\nParallelism Analysis:")
    print(f"  Single-thread throughput: {results[0]['throughput']:.0f} iter/sec")
    print(f"  Multi-thread throughput: {overall_throughput:.0f} iter/sec")
    print(f"  Parallelism factor: {parallelism_ratio:.2f}x")

    if parallelism_ratio > 1.5:
        print("  ✓ Threads are executing in parallel!")
    else:
        print("  ⚠️  Limited parallelism (likely due to GIL)")


def check_gil_status() -> dict:
    """Check the current GIL configuration."""
    info = {
        "gil_enabled": sys._is_gil_enabled(),
        "python_version": sys.version,
        "thread_info": threading.current_thread().name,
    }

    # Check if this is a free-threaded build
    try:
        # In free-threaded builds, there are additional attributes
        info["supports_free_threading"] = hasattr(sys, "_is_gil_enabled")
    except Exception as e:
        info["error"] = str(e)

    return info


def cpu_intensive_work():
    """Simple CPU-intensive work for monitoring."""
    total = 0
    for i in range(1000):
        total += i**2
    return total


if __name__ == "__main__":
    main()
