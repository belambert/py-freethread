# Python Free-Threading Demo

Demonstrates Python 3.14's free-threading capabilities (PEP 703), which allows Python to run without the Global Interpreter Lock (GIL), enabling true parallel execution of threads.

## Setup

### Install Python Versions

Install both standard and free-threaded Python 3.14:

```bash
# Standard Python 3.14 (with GIL)
uv python install 3.14

# Free-threaded Python 3.14 (without GIL)
uv python install 3.14t
```

### Verify Installation

Check GIL status for each version:

```bash
# Standard Python - should show "True"
uv run --python 3.14 python -c "import sys; print(f'GIL enabled: {sys._is_gil_enabled()}')"

# Free-threaded Python - should show "False"
uv run --python 3.14t python -c "import sys; print(f'GIL enabled: {sys._is_gil_enabled()}')"
```

## Examples

Each example can be run with either Python version to compare behavior.

### 1. GIL Control and Monitoring

Check GIL status and measure thread parallelism.

```bash
# With GIL (standard Python)
uv run --python 3.14 python -m py_freethread.gil_control

# Without GIL (free-threaded Python)
uv run --python 3.14t python -m py_freethread.gil_control
```

**Expected**: Standard shows limited parallelism (~1-1.5x), free-threaded shows true parallelism (~3-4x on 4 cores).

### 2. CPU-Bound Workload

Fibonacci calculations demonstrate CPU parallelism benefits.

```bash
# With GIL (standard Python)
uv run --python 3.14 python -m py_freethread.cpu_bound

# Without GIL (free-threaded Python)
uv run --python 3.14t python -m py_freethread.cpu_bound
```

**Expected**: Standard shows ~1.0x speedup (no parallel benefit), free-threaded shows ~3-4x speedup.

### 3. I/O-Bound Workload

Simulated I/O operations with threading.

```bash
# With GIL (standard Python)
uv run --python 3.14 python -m py_freethread.io_bound

# Without GIL (free-threaded Python)
uv run --python 3.14t python -m py_freethread.io_bound
```

**Expected**: Both show ~4x speedup. I/O operations release the GIL, so both versions perform similarly.

## Key Takeaways

- **CPU-bound tasks**: Free-threading enables true parallelism, providing near-linear speedup
- **I/O-bound tasks**: Threading works well regardless of GIL (GIL is released during I/O)
- **Thread safety**: Without GIL, explicit synchronization (locks) is required for shared mutable state

## References

- [PEP 703 – Making the Global Interpreter Lock Optional](https://peps.python.org/pep-0703/)
- [Python 3.13+ Free-threading Documentation](https://docs.python.org/3.13/howto/free-threading-python.html)
