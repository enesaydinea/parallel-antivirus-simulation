import random
import time
from multiprocessing import Pool

# ================================
# 1) SAHTE DOSYA ÜRETİCİSİ
# ================================
def generate_fake_files(n, virus_rate=0.00001):
    exts = [
        ("exe", 5),
        ("dll", 4),
        ("msi", 4),
        ("pdf", 2),
        ("docx", 2),
        ("jpg", 1),
        ("txt", 1),
    ]

    files = []
    for i in range(n):
        ext, ext_risk = random.choice(exts)
        size_mb = random.uniform(0.1, 500.0)
        is_download = random.choice([0, 1])
        last_modified_days = random.randint(0, 365 * 3)

        risk = (
            3 * ext_risk +
            2 * is_download +
            (size_mb / 100.0) +
            (1 / (1 + last_modified_days))
        )

        infected = random.random() < virus_rate

        files.append({
            "file_name": f"file_{i}.{ext}",
            "risk": risk,
            "infected": infected
        })

    return files


# ================================
# 2) SIRALAMA
# ================================
def sort_by_risk_desc(files):
    return sorted(files, key=lambda x: x["risk"], reverse=True)


# ================================
# 3) TARAMA
# ================================
def scan_chunk(args):
    chunk, loops = args
    found = []

    for f in chunk:
        x = f["risk"]
        for _ in range(loops):  # CPU-bound iş
            x = (x * 1.000001) + 0.0000001

        if f["infected"]:
            found.append(f)

    return found


def serial_scan(files, loops):
    start = time.perf_counter()
    found = scan_chunk((files, loops))
    end = time.perf_counter()
    return found, end - start


def parallel_scan(files, num_workers, loops):
    n = len(files)
    chunk_size = n // num_workers
    chunks = []

    for i in range(num_workers):
        start_i = i * chunk_size
        end_i = n if i == num_workers - 1 else (i + 1) * chunk_size
        chunks.append(files[start_i:end_i])

    start = time.perf_counter()
    with Pool(num_workers) as pool:
        results = pool.map(scan_chunk, [(ch, loops) for ch in chunks])

    found = []
    for r in results:
        found.extend(r)

    end = time.perf_counter()
    return found, end - start


# ================================
# 4) MAIN – FULL SCAN
# ================================
if __name__ == "__main__":
    N_FILES = 2_000_000
    NUM_WORKERS = 8
    SCAN_LOOPS = 800
    VIRUS_RATE = 0.00001

    print(f"Toplam dosya sayısı        : {N_FILES}")
    print(f"Kullanılan worker (process): {NUM_WORKERS}")

    print("\n[0] Dosyalar üretiliyor...")
    files = generate_fake_files(N_FILES, VIRUS_RATE)

    print("\n[1] Risk sıralaması yapılıyor...")
    files_sorted = sort_by_risk_desc(files)

    print(f"\n[2] FULL SCAN: {len(files_sorted)} dosya taranacak")

    print("\n[3] SERİ TARAMA...")
    serial_found, t_serial = serial_scan(files_sorted, SCAN_LOOPS)
    print(f"Seri süre: {t_serial:.4f}s | Virüs: {len(serial_found)}")

    print("\n[4] PARALEL TARAMA...")
    parallel_found, t_parallel = parallel_scan(files_sorted, NUM_WORKERS, SCAN_LOOPS)
    print(f"Paralel süre: {t_parallel:.4f}s | Virüs: {len(parallel_found)}")

    print("\n==== SONUÇ ====")
    print(f"Seri süre    : {t_serial:.4f} s")
    print(f"Paralel süre : {t_parallel:.4f} s")
    print(f"Hızlanma     : {(t_serial / t_parallel):.2f}x")

    if parallel_found:
        print("\n⚠️ BULUNAN VİRÜSLER:")
        for f in parallel_found:
            print(f"- {f['file_name']} | risk={f['risk']:.2f}")
    else:
        print("\n✅ Virüs bulunamadı.")
