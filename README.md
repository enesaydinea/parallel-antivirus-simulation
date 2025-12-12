# parallel-antivirus-simulation
Parallel antivirus scan simulation using Python multiprocessing
# Parallel Antivirus Scan Simulation

This project simulates a full antivirus scan using Python’s multiprocessing
to compare serial and parallel performance on a large synthetic dataset.

---

## 🚀 Project Overview

Modern antivirus software must analyze millions of files quickly.  
This simulation creates a large synthetic dataset of file metadata and performs:

- **Serial scanning**
- **Parallel scanning** using Python multiprocessing

The goal is to demonstrate the performance benefit of parallel processing.

---

## 🧪 Experiment Setup

| Parameter | Value |
|-----------|-------|
| Number of synthetic files | **2,000,000** |
| Scan mode | Full Scan |
| Worker processes | **8** |
| Scan complexity (loops) | **800** |
| Virus ratio (simulated) | **0.00001** |

---

## 📊 Results

Measured using `time.perf_counter()`:

| Mode | Time (seconds) |
|------|----------------|
| Serial scan | **38.52 s** |
| Parallel scan | **9.03 s** |
| Speedup | **≈ 4.26×** |

---

## 🧠 How It Works

1. **Data Generation**  
   Produces a synthetic list of file metadata, including:
   - file name
   - risk score
   - simulated “infected” flag

2. **Risk Sorting**  
   Files are sorted by computed risk before scanning.

3. **Scanning**  
   - Serial: One process scans all files.
   - Parallel: Files are split across `NUM_WORKERS` and scanned concurrently.

4. **Performance Measurement**  
   Execution times are measured for both modes and compared.

---

## 🛠️ How to Run

```bash
python parallel_antivirus.py
