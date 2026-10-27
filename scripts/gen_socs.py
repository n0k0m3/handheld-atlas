"""Fill data/socs/*.json from the table below. Run: python3 -I gen_socs.py <repo>/data/socs [extra-id ...]"""
import json
import pathlib
import sys

D = "2026-10-27"
CAVEAT = "PassMark scores mix TDPs and host devices; treat them as a rough guide only."
TF_NOTE = ("igpu.tflops_fp32 = shaders x 2 FLOP x vendor max GPU clock "
           "(single-issue FMA; RDNA 3 dual-issue is not counted).")
INTEL_TDP = ("Intel tdp_w: default = Processor Base Power, min = Minimum Assured Power, "
             "max = Maximum Turbo Power (PL2); PL2 is not comparable to an AMD cTDP maximum.")
NPU0 = "npu_tops 0: the vendor spec page lists no AI engine (NPU absent or fused off)."

AMD = "https://www.amd.com/en/products/processors/"
TC = "https://www.techpowerup.com/cpu-specs/"
TG = "https://www.techpowerup.com/gpu-specs/"
PC = "https://www.cpubenchmark.net/cpu.php?cpu="
PG = "https://www.videocardbenchmark.net/gpu.php?gpu="

# Shaders per CU / Xe-core used by tflops().
SHADERS = {"AMD": 64, "Intel": 128}
DUAL_ISSUE_RDNA3 = False  # set True to count RDNA 3 / 3.5 dual-issue (x2), as TPU does for RDNA 3 only


def tflops(fam, units, mhz, arch):
    mult = 2 if (DUAL_ISSUE_RDNA3 and arch.startswith("RDNA 3")) else 1
    return round(units * SHADERS[fam] * 2 * mult * mhz / 1e6, 2)


# PassMark rows: (name, mark, single, samples, href). GPU rows: (name, g3d, samples, href).
CPU = {
    "z1e": ("AMD Ryzen Z1 Extreme", 24556, 3522, 1252, "AMD+Ryzen+Z1+Extreme&id=5508"),
    "z1": ("AMD Ryzen Z1", 18258, 3577, 65, "AMD+Ryzen+Z1&id=5756"),
    "z2": ("AMD Ryzen Z2", 25765, 3547, 12, "AMD+Ryzen+Z2&id=7086"),
    "z2e": ("AMD Ryzen Z2 Extreme", 23200, 3899, 33, "AMD+Ryzen+Z2+Extreme&id=6816"),
    "aiz2e": ("AMD Ryzen AI Z2 Extreme", 22340, 3568, 105, "AMD+Ryzen+AI+Z2+Extreme&id=6963"),
    "z2go": ("AMD Ryzen Z2 Go", 11090, 2833, 22, "AMD+Ryzen+Z2+Go&id=6563"),
    "z2a": ("AMD Ryzen Z2 A", 10008, 2295, 22, "AMD+Ryzen+Z2+A&id=6967"),
    "0932": ("AMD Custom APU 0932", 9342, 2201, 27, "AMD+Custom+APU+0932&id=6154"),
    "6800u": ("AMD Ryzen 7 6800U", 20651, 3197, 553, "AMD+Ryzen+7+6800U&id=4923"),
    "7840u": ("AMD Ryzen 7 7840U", 24379, 3535, 567, "AMD+Ryzen+7+7840U&id=5322"),
    "7640u": ("AMD Ryzen 5 7640U", 20219, 3408, 143, "AMD+Ryzen+5+7640U&id=5639"),
    "8840u": ("AMD Ryzen 7 8840U", 23366, 3539, 609, "AMD+Ryzen+7+8840U&id=6003"),
    "8840hs": ("AMD Ryzen 7 8840HS", 24509, 3568, 811, "AMD+Ryzen+7+8840HS&id=6016"),
    "8845hs": ("AMD Ryzen 7 8845HS", 28251, 3717, 4052, "AMD+Ryzen+7+8845HS&id=5915"),
    "hx370": ("AMD Ryzen AI 9 HX 370", 34945, 3937, 3297, "AMD+Ryzen+AI+9+HX+370&id=6143"),
    "365": ("AMD Ryzen AI 9 365", 30326, 3857, 947, "AMD+Ryzen+AI+9+365&id=6180"),
    "395": ("AMD Ryzen AI Max+ 395", 54782, 4144, 1240, "AMD+Ryzen+AI+Max%2B+395&id=6403"),
    "385": ("AMD Ryzen AI Max 385", 33726, 4072, 27, "AMD+Ryzen+AI+Max+385&id=6602"),
    "388": ("AMD RYZEN AI MAX+ 388", 32831, 4119, 24, "AMD+RYZEN+AI+MAX%2B+388&id=7006"),
    "135h": ("Intel Core Ultra 5 135H", 21904, 3458, 488, "Intel+Core+Ultra+5+135H&id=5817"),
    "155h": ("Intel Core Ultra 7 155H", 24418, 3400, 6992, "Intel+Core+Ultra+7+155H&id=5677"),
    "258v": ("Intel Core Ultra 7 258V", 18877, 4010, 2339, "Intel+Core+Ultra+7+258V&id=6281"),
    "g3e": ("Intel Arc G3 Extreme", 28624, 4056, 9, "Intel+Arc+G3+Extreme&id=7300"),
    "6600u": ("AMD Ryzen 5 6600U", 16871, 3075, 96, "AMD+Ryzen+5+6600U&id=4949"),
    "5560u": ("AMD Ryzen 5 5560U", 15173, 2830, 409, "AMD+Ryzen+5+5560U&id=4883"),
    "5825u": ("AMD Ryzen 7 5825U", 17775, 2988, 3284, "AMD+Ryzen+7+5825U&id=4788"),
    "5800u": ("AMD Ryzen 7 5800U", 17934, 2982, 995, "AMD+Ryzen+7+5800U&id=4102"),
    "hx470": ("AMD Ryzen AI 9 HX 470", 37238, 4139, 162, "AMD+Ryzen+AI+9+HX+470&id=7087"),
    "8640u": ("AMD Ryzen 5 8640U", 19859, 3459, 44, "AMD+Ryzen+5+8640U&id=6089"),
    "1260p": ("Intel Core i7-1260P", 16364, 3188, 2924, "Intel+Core+i7-1260P&id=4707"),
    "255h": ("Intel Core Ultra 7 255H", 30792, 4309, 2292, "Intel+Core+Ultra+7+255H&id=6471"),
    "125h": ("Intel Core Ultra 5 125H", 19913, 3311, 2470, "Intel+Core+Ultra+5+125H&id=5777"),
    "228v": ("Intel Core Ultra 5 228V", 18121, 3790, 209, "Intel+Core+Ultra+5+228V&id=6364"),
    "1360p": ("Intel Core i7-1360P", 18215, 3406, 2102, "Intel+Core+i7-1360P&id=5198"),
    "1195g7": ("Intel Core i7-1195G7 @ 2.90GHz", 10349, 2940, 864, "Intel+Core+i7-1195G7+%40+2.90GHz&id=4514"),
}
GPU = {
    "z1e": ("AMD Ryzen Z1 Extreme", 6419, 903, "AMD+Ryzen+Z1+Extreme&id=4918"),
    "740m": ("Radeon 740M", 2940, 2410, "Radeon+740M&id=4926"),
    "760m": ("Radeon 760M", 5294, 2782, "Radeon+760M&id=4902"),
    "780m": ("Radeon 780M", 6724, 12851, "Radeon+780M&id=4818"),
    "880m": ("Radeon 880M", 7597, 849, "Radeon+880M&id=5123"),
    "890m": ("Radeon 890M", 8061, 2367, "Radeon+890M&id=5113"),
    "8050s": ("Radeon 8050S", 16468, 206, "Radeon+8050S&id=5322"),
    "8060s": ("Radeon 8060S", 18056, 1457, "Radeon+8060S&id=5327"),
    "6800u": ("Radeon Ryzen 7 6800U", 4226, 386, "Radeon+Ryzen+7+6800U&id=4648"),
    "z2go": ("Radeon Ryzen Z2 Go", 4733, 18, "Radeon+Ryzen+Z2+Go&id=5988"),
    "0405": ("Custom GPU 0405", 2949, 118, "Custom+GPU+0405&id=4528"),
    "0932": ("Custom GPU 0932", 3194, 19, "Custom+GPU+0932&id=5164"),
    "arc": ("Intel Arc", 5478, 7493, "Intel+Arc&id=4955"),
    "140v": ("Intel Arc 140V GPU", 5146, 4843, "Intel+Arc+140V+GPU&id=5176"),
    "b390": ("Intel Arc B390 GPU", 9001, 604, "Intel+Arc+B390+GPU&id=7571"),
    "b370": ("Intel Arc B370 GPU", 8483, 57, "Intel+Arc+B370+GPU&id=7972"),
    "6600u": ("Radeon Ryzen 5 6600U", 3221, 81, "Radeon+Ryzen+5+6600U&id=4675"),
    "5560u": ("Radeon Ryzen 5 5560U", 2028, 341, "Radeon+Ryzen+5+5560U&id=4555"),
    "5825u": ("Radeon Ryzen 7 5825U", 2397, 2593, "Radeon+Ryzen+7+5825U&id=4668"),
    "5800u": ("Radeon Ryzen 7 5800U", 2369, 708, "Radeon+Ryzen+7+5800U&id=4464"),
    "irisxe": ("Intel Iris Xe", 2587, 73915, "Intel+Iris+Xe&id=4265"),
    "140t": ("Intel Arc 140T GPU", 6586, 2295, "Intel+Arc+140T+GPU&id=5577"),
    "130v": ("Intel Arc 130V GPU", 4517, 1456, "Intel+Arc+130V+GPU&id=5185"),
}


def src(field, url, note=None):
    return {"field": field, "url": url, "accessed": D, "note": note}


def row(id_, vendor, name, codename, cores, threads, mix, arch, base, boost, tdp, pnm, pnote,
        npu, mem, launch, ig, cpu, gpu, mapping, notes, sources, fam="AMD"):
    ig_name, ig_units, ig_arch, ig_mhz, ig_tf = ig
    if ig_tf is None:
        ig_tf = tflops(fam, ig_units, ig_mhz, ig_arch)
    c, g = CPU[cpu], GPU[gpu]
    return {
        "id": id_, "vendor": vendor, "name": name, "codename": codename,
        "cores": cores, "threads": threads, "core_mix": mix, "cpu_arch": arch,
        "base_ghz": base, "boost_ghz": boost,
        "tdp_w": {"default": tdp[0], "min": tdp[1], "max": tdp[2]},
        "process_nm": pnm, "process_note": pnote, "npu_tops": npu, "memory": mem,
        "launch_date": launch,
        "igpu": {"name": ig_name, "cu": ig_units, "arch": ig_arch, "clock_mhz": ig_mhz, "tflops_fp32": ig_tf},
        "passmark": {
            "cpu_mark": c[1], "single_thread": c[2], "cpu_samples": c[3], "cpu_url": PC + c[4],
            "g3d_mark": g[1], "g3d_samples": g[2], "gpu_url": PG + g[3],
            "fetched": D, "mapping_note": mapping,
        },
        "notes": " ".join(x for x in (notes, TF_NOTE, CAVEAT) if x),
        "unresolved": [],
        "sources": sources,
    }


def pm_sources(cpu, gpu):
    return [src("passmark.cpu_mark", PC + CPU[cpu][4], "CPU Mark, single thread rating and samples"),
            src("passmark.g3d_mark", PG + GPU[gpu][3], "G3D Mark and samples")]


def tpu_gpu(slug, listed):
    return src("igpu.tflops_fp32", TG + slug, f"cross-check only; TPU lists {listed}")


ROWS = {}

# ---------- AMD Ryzen Z handheld ----------
Z = AMD + "handhelds/ryzen-z-series/"
ROWS["z1-extreme"] = row(
    "z1-extreme", "AMD", "Ryzen Z1 Extreme", "Phoenix", 8, 16, "8x Zen 4", "Zen 4", 3.3, 5.1, (28, 9, 30),
    4, "TSMC 4nm (same Phoenix die as the Ryzen 7 7840U)", 0, "DDR5-5600, LPDDR5X-7500, dual-channel", "2023-05",
    ("Radeon 780M-class (12 CU)", 12, "RDNA 3", 2900, None), "z1e", "z1e",
    "CPU and GPU: exact PassMark entries 'AMD Ryzen Z1 Extreme'. The GPU entry is the Z1 Extreme iGPU (reported as "
    "'AMD Radeon Graphics'). The laptop twin 'Radeon 780M' scores 6724 G3D (12851 samples).",
    "AMD names the iGPU only 'AMD Radeon Graphics'; TPU equates it to the Radeon 780M. " + NPU0,
    [src("*", Z + "z1-series/z1-extreme.html", "AMD spec page: cores, clocks, TDP, iGPU CU and clock")]
    + pm_sources("z1e", "z1e")
    + [src("launch_date", TC + "ryzen-z1-extreme.c3276", "TPU: release May 2023; also process_nm and memory"),
       src("process_nm", TC + "ryzen-z1-extreme.c3276", "TPU: TSMC 4 nm"),
       src("memory", TC + "ryzen-z1-extreme.c3276", "TPU: DDR5-5600, LPDDR5X-7500"),
       tpu_gpu("ryzen-z1-extreme-gpu.c4157", "8.294 TFLOPS (counts RDNA 3 dual-issue at 2700 MHz)")])

ROWS["z1"] = row(
    "z1", "AMD", "Ryzen Z1", "Phoenix 2", 6, 12, "2x Zen 4 + 4x Zen 4c", "Zen 4 / Zen 4c", 3.2, 4.9, (28, 9, 30),
    4, "TSMC 4nm", 0, "DDR5-5600, LPDDR5X-7500, dual-channel", "2023-05",
    ("Radeon 740M-class (4 CU)", 4, "RDNA 3", 2800, None), "z1", "740m",
    "CPU: exact entry 'AMD Ryzen Z1' (65 samples). GPU: no Z1 iGPU entry; stand-in 'Radeon 740M' "
    "(laptop twin with 4 CU RDNA 3).",
    "Zen 4 cores: 3.7 GHz base; Zen 4c cores: 3.0 GHz base, up to 3.5 GHz. Codename set to Phoenix 2 "
    "(the 2+4 core die); the stub said Phoenix. " + NPU0,
    [src("*", Z + "z1-series/z1.html", "AMD spec page: cores, clocks, TDP, iGPU CU and clock")]
    + pm_sources("z1", "740m")
    + [src("codename", TC + "ryzen-z1.c3287", "TPU lists the Z1 under Phoenix2"),
       src("launch_date", TC + "ryzen-z1.c3287", "TPU: release May 2023"),
       src("process_nm", TC + "ryzen-z1.c3287", "TPU: TSMC 4 nm"),
       src("memory", TC + "ryzen-z1.c3287", "TPU: DDR5-5600, LPDDR5X-7500"),
       tpu_gpu("ryzen-z1-gpu.c4158", "2.560 TFLOPS (counts RDNA 3 dual-issue at 2500 MHz)")])

ROWS["z2"] = row(
    "z2", "AMD", "Ryzen Z2", "Hawk Point", 8, 16, "8x Zen 4", "Zen 4", 3.3, 5.1, (28, 15, 30),
    4, "TSMC 4nm", 0, "DDR5-5600, LPDDR5X-7500, dual-channel", "2025-01-06",
    ("Radeon 780M-class (12 CU)", 12, "RDNA 3", 2700, None), "z2", "780m",
    "CPU: exact entry 'AMD Ryzen Z2' (only 12 samples). GPU: no Z2 iGPU entry; stand-in 'Radeon 780M' "
    "(laptop twin with the same 12 CU RDNA 3 at 2.7 GHz).",
    "Separate chip from the Ryzen Z2 Extreme and Ryzen AI Z2 Extreme. " + NPU0,
    [src("*", Z + "z2-series/z2.html", "AMD spec page: cores, clocks, TDP, iGPU CU and clock")]
    + pm_sources("z2", "780m")
    + [src("codename", TC + "ryzen-z2.c4603", "TPU: Hawk Point"),
       src("launch_date", TC + "ryzen-z2.c4603", "TPU: release Jan 6th, 2025"),
       src("process_nm", TC + "ryzen-z2.c4603", "TPU: TSMC 4 nm"),
       src("memory", TC + "ryzen-z2.c4603", "TPU: DDR5-5600, LPDDR5X-7500"),
       tpu_gpu("ryzen-z2-gpu.c4303", "8.294 TFLOPS (counts RDNA 3 dual-issue at 2700 MHz)")])

ROWS["z2-extreme"] = row(
    "z2-extreme", "AMD", "Ryzen Z2 Extreme", "Strix Point", 8, 16, "3x Zen 5 + 5x Zen 5c", "Zen 5 / Zen 5c", 2.0, 5.0,
    (28, 15, 35), 4, "TSMC 4nm", 0, "DDR5-5600, LPDDR5X-8000, dual-channel", "2025-01-06",
    ("Radeon 890M-class (16 CU)", 16, "RDNA 3.5", 2900, None), "z2e", "890m",
    "CPU: exact entry 'AMD Ryzen Z2 Extreme' (33 samples). GPU: no Z2 Extreme iGPU entry; stand-in 'Radeon 890M' "
    "(laptop twin with 16 CU RDNA 3.5; laptop samples often run at higher TDP).",
    "Zen 5c cores run up to 3.3 GHz. Separate chip from the Ryzen AI Z2 Extreme, which exposes a 50 TOPS NPU. " + NPU0,
    [src("*", Z + "z2-series/z2-extreme.html", "AMD spec page: core mix, clocks, TDP, iGPU CU and clock")]
    + pm_sources("z2e", "890m")
    + [src("launch_date", TC + "ryzen-z2-extreme.c4602", "TPU: release Jan 6th, 2025"),
       src("process_nm", TC + "ryzen-z2-extreme.c4602", "TPU: TSMC 4 nm"),
       src("memory", TC + "ryzen-z2-extreme.c4602", "TPU: DDR5-5600, LPDDR5X-8000"),
       tpu_gpu("ryzen-z2-extreme-gpu.c4304", "5.939 TFLOPS")])

ROWS["z2-ai-extreme"] = row(
    "z2-ai-extreme", "AMD", "Ryzen AI Z2 Extreme", "Strix Point", 8, 16, "3x Zen 5 + 5x Zen 5c", "Zen 5 / Zen 5c",
    2.0, 5.0, (28, 15, 35), 4, "TSMC 4nm", 50, "DDR5-5600, LPDDR5X-8000, dual-channel", "2025-06-08",
    ("Radeon 890M-class (16 CU)", 16, "RDNA 3.5", 2900, None), "aiz2e", "890m",
    "CPU: exact entry 'AMD Ryzen AI Z2 Extreme' (105 samples). GPU: no AI Z2 Extreme iGPU entry; stand-in "
    "'Radeon 890M' (laptop twin with 16 CU RDNA 3.5; laptop samples often run at higher TDP).",
    "Same core and GPU layout as the Ryzen Z2 Extreme, plus a 50 TOPS NPU. Zen 5c cores run up to 3.3 GHz.",
    [src("*", Z + "z2-series/ai-z2-extreme.html", "AMD spec page: core mix, clocks, TDP, iGPU, NPU 50 TOPS")]
    + pm_sources("aiz2e", "890m")
    + [src("launch_date", TC + "ryzen-ai-z2-extreme.c4601", "TPU: release Jun 8th, 2025"),
       src("process_nm", TC + "ryzen-ai-z2-extreme.c4601", "TPU: TSMC 4 nm"),
       src("memory", TC + "ryzen-ai-z2-extreme.c4601", "TPU: DDR5-5600, LPDDR5X-8000"),
       tpu_gpu("ryzen-ai-z2-extreme-gpu.c4305", "5.939 TFLOPS")])

ROWS["z2-go"] = row(
    "z2-go", "AMD", "Ryzen Z2 Go", "Rembrandt", 4, 8, "4x Zen 3+", "Zen 3+", 3.0, 4.3, (28, 15, 30),
    6, "TSMC 6nm", 0, "DDR5-4800, LPDDR5-6400, dual-channel", "2025-01-06",
    ("Radeon (12 CU RDNA 2)", 12, "RDNA 2", 2200, None), "z2go", "z2go",
    "CPU and GPU: exact entries 'AMD Ryzen Z2 Go' (22 samples) and 'Radeon Ryzen Z2 Go' (only 18 samples). "
    "The laptop twin 'Radeon Ryzen 7 6800U' (680M) scores 4226 G3D with 386 samples.",
    NPU0,
    [src("*", Z + "z2-series/z2-go.html", "AMD spec page: cores, clocks, TDP, iGPU CU and clock")]
    + pm_sources("z2go", "z2go")
    + [src("launch_date", TC + "ryzen-z2-go.c4604", "TPU: release Jan 6th, 2025"),
       src("process_nm", TC + "ryzen-z2-go.c4604", "TPU: TSMC 6 nm, Rembrandt"),
       src("memory", TC + "ryzen-z2-go.c4604", "TPU: DDR5-4800, LPDDR5-6400"),
       tpu_gpu("ryzen-z2-go-gpu.c4307", "3.379 TFLOPS")])

ROWS["z2-a"] = row(
    "z2-a", "AMD", "Ryzen Z2 A", "Van Gogh", 4, 8, "4x Zen 2", "Zen 2", 2.8, 3.8, (15, 6, 20),
    7, "TSMC 7nm (Van Gogh, as the Steam Deck LCD APU)", 0, "LPDDR5-6400", "2025-06-08",
    ("Radeon (8 CU RDNA 2)", 8, "RDNA 2", 1800, None), "z2a", "0405",
    "CPU: exact entry 'AMD Ryzen Z2 A' (22 samples); the brief expected a Steam Deck stand-in, but Z2 A has its "
    "own entry. GPU: no Z2 A iGPU entry; stand-in 'Custom GPU 0405' = Steam Deck LCD iGPU (same Van Gogh "
    "8 CU RDNA 2; Z2 A clocks to 1.8 GHz, Deck to 1.6 GHz).",
    NPU0,
    [src("*", Z + "z2-series/z2-a.html", "AMD spec page: cores, clocks, TDP, iGPU CU and clock")]
    + pm_sources("z2a", "0405")
    + [src("launch_date", TC + "ryzen-z2-a.c4565", "TPU: release Jun 8th, 2025"),
       src("process_nm", TC + "ryzen-z2-a.c4565", "TPU: TSMC 7 nm, Van Gogh"),
       src("memory", TC + "ryzen-z2-a.c4565", "TPU: LPDDR5-6400"),
       tpu_gpu("ryzen-z2-a-gpu.c4306", "1.843 TFLOPS")])

# ---------- Valve ----------
ROWS["steam-deck-apu-lcd"] = row(
    "steam-deck-apu-lcd", "Valve/AMD", "Steam Deck APU (LCD)", "Aerith", 4, 8, "4x Zen 2", "Zen 2", 2.4, 3.5,
    (15, 4, 15), 7, "TSMC 7nm (Valve: 7 nm; foundry per TPU)", 0,
    "16 GB LPDDR5-5500 on-board, quad 32-bit channels", "2022-02-25",
    ("AMD Custom GPU 0405", 8, "RDNA 2", 1600, 1.6), "0932", "0405",
    "CPU: PassMark has no 'AMD Custom APU 0405' entry (cpu.php and cpu_lookup.php return 404; it is absent from "
    "the full CPU list). Stand-in = 'AMD Custom APU 0932' (Steam Deck OLED APU: same 4C/8T Zen 2 at "
    "2.4-3.5 GHz, 6 nm). GPU: exact entry 'Custom GPU 0405'.",
    "Valve gives 4-15 W APU power; default set to the 15 W maximum. AMD part number 100-000000405 (TPU). "
    "tflops_fp32 is Valve's stated 1.6 TFLOPS. " + NPU0,
    [src("*", "https://www.steamdeck.com/en/tech/deck", "Valve tech specs: APU, CPU/GPU clocks, 1.6 TFLOPS, 4-15 W, RAM")]
    + pm_sources("0932", "0405")
    + [src("launch_date", TC + "steam-deck-cpu-lcd.c3397", "TPU: release Feb 25th, 2022; part 100-000000405"),
       src("process_note", TC + "steam-deck-cpu-lcd.c3397", "TPU: TSMC 7 nm"),
       tpu_gpu("steam-deck-gpu.c3897", "1.638 TFLOPS")])

ROWS["steam-deck-apu-oled"] = row(
    "steam-deck-apu-oled", "Valve/AMD", "Steam Deck APU (OLED)", "Sephiroth", 4, 8, "4x Zen 2", "Zen 2", 2.4, 3.5,
    (15, 4, 15), 6, "TSMC 6nm (Valve: 6 nm; foundry per TPU)", 0,
    "16 GB LPDDR5-6400 on-board, quad 32-bit channels", "2023-11-09",
    ("AMD Custom GPU 0932", 8, "RDNA 2", 1600, 1.6), "0932", "0932",
    "CPU and GPU: exact entries 'AMD Custom APU 0932' (27 samples) and 'Custom GPU 0932' (19 samples). "
    "The brief assumed the OLED shares the LCD '0405' entry; the OLED APU is part 100-000000932 and has its own entries.",
    "igpu.name changed from the stub's 'AMD Custom GPU 0405' to 'AMD Custom GPU 0932' (OLED part 100-000000932 per TPU). "
    "Valve gives 4-15 W APU power; default set to the 15 W maximum. tflops_fp32 is Valve's stated 1.6 TFLOPS. " + NPU0,
    [src("*", "https://www.steamdeck.com/en/tech/oled", "Valve tech specs (OLED): 6 nm APU, clocks, 1.6 TFLOPS, 4-15 W, RAM")]
    + pm_sources("0932", "0932")
    + [src("launch_date", TC + "steam-deck-cpu-oled.c3398", "TPU: release Nov 9th, 2023; part 100-000000932"),
       src("igpu.name", TC + "steam-deck-cpu-oled.c3398", "part number 100-000000932 matches PassMark 'Custom GPU 0932'"),
       src("process_note", TC + "steam-deck-cpu-oled.c3398", "TPU: TSMC 6 nm"),
       tpu_gpu("steam-deck-oled-gpu.c4185", "1.638 TFLOPS")])

# ---------- AMD laptop ----------
L = AMD + "laptop/ryzen/"
ROWS["r7-6800u"] = row(
    "r7-6800u", "AMD", "Ryzen 7 6800U", "Rembrandt", 8, 16, "8x Zen 3+", "Zen 3+", 2.7, 4.7, (15, 15, 28),
    6, "TSMC 6nm FinFET", 0, "DDR5-4800, LPDDR5-6400, dual-channel, up to 64 GB", "2022-04-19",
    ("Radeon 680M", 12, "RDNA 2", 2200, None), "6800u", "6800u",
    "CPU: exact entry. GPU: chip-named entry 'Radeon Ryzen 7 6800U' (the iGPU reports as 'AMD Radeon Graphics'), "
    "chosen over the generic 'Radeon 680M' entry (4016 G3D, only 10 samples).",
    "AMD gives only a 15-28 W cTDP; the 15 W default is from TPU. " + NPU0,
    [src("*", "https://www.amd.com/en/support/downloads/drivers.html/processors/ryzen/ryzen-6000-series/amd-ryzen-7-6800u.html",
         "the AMD product page returns 404; this AMD driver page carries the full spec table")]
    + pm_sources("6800u", "6800u")
    + [src("tdp_w.default", TC + "ryzen-7-6800u.c2523", "TPU: TDP 15 W"),
       tpu_gpu("radeon-680m.c3871", "3.379 TFLOPS")])

ROWS["r7-7840u"] = row(
    "r7-7840u", "AMD", "Ryzen 7 7840U", "Phoenix", 8, 16, "8x Zen 4", "Zen 4", 3.3, 5.1, (28, 15, 30),
    4, "TSMC 4nm FinFET", 10, "DDR5-5600, LPDDR5X-7500, dual-channel, up to 256 GB", "2023-05-03",
    ("Radeon 780M", 12, "RDNA 3", 2700, None), "7840u", "780m",
    "CPU and GPU: exact entries.",
    "AMD lists the NPU at up to 10 TOPS (32 TOPS overall).",
    [src("*", L + "7000-series/amd-ryzen-7-7840u.html", "AMD spec page: all CPU, memory, NPU and iGPU fields, launch 05/03/2023")]
    + pm_sources("7840u", "780m")
    + [tpu_gpu("radeon-780m.c4020", "8.294 TFLOPS (counts RDNA 3 dual-issue)")])

ROWS["r5-7640u"] = row(
    "r5-7640u", "AMD", "Ryzen 5 7640U", "Phoenix", 6, 12, "6x Zen 4", "Zen 4", 3.5, 4.9, (28, 15, 30),
    4, "TSMC 4nm FinFET", 10, "DDR5-5600, LPDDR5X-7500, dual-channel, up to 256 GB", "2023-05-03",
    ("Radeon 760M", 8, "RDNA 3", 2600, None), "7640u", "760m",
    "CPU and GPU: exact entries.",
    "AMD lists the NPU at up to 10 TOPS (25 TOPS overall).",
    [src("*", L + "7000-series/amd-ryzen-5-7640u.html", "AMD spec page: all CPU, memory, NPU and iGPU fields, launch 05/03/2023")]
    + pm_sources("7640u", "760m")
    + [tpu_gpu("radeon-760m.c4022", "5.323 TFLOPS (counts RDNA 3 dual-issue at 2599 MHz)")])

ROWS["r7-8840u"] = row(
    "r7-8840u", "AMD", "Ryzen 7 8840U", "Hawk Point", 8, 16, "8x Zen 4", "Zen 4", 3.3, 5.1, (28, 15, 30),
    4, "TSMC 4nm FinFET", 16, "DDR5-5600, LPDDR5X-7500, dual-channel, up to 96 GB DDR5 / 64 GB LPDDR5X", "2023-12-06",
    ("Radeon 780M", 12, "RDNA 3", 2700, None), "8840u", "780m",
    "CPU and GPU: exact entries.",
    "AMD lists the NPU at up to 16 TOPS (38 TOPS overall).",
    [src("*", L + "8000-series/amd-ryzen-7-8840u.html", "AMD spec page: CPU, memory, NPU and iGPU fields (no launch date)")]
    + pm_sources("8840u", "780m")
    + [src("launch_date", TC + "ryzen-7-8840u.c3402", "TPU: release Dec 6th, 2023"),
       tpu_gpu("radeon-780m.c4221", "8.294 TFLOPS (Hawk Point 780M; counts RDNA 3 dual-issue)")])

ROWS["r7-8840hs"] = row(
    "r7-8840hs", "AMD", "Ryzen 7 8840HS", "Hawk Point", 8, 16, "8x Zen 4", "Zen 4", 3.3, 5.1, (28, 20, 30),
    4, "TSMC 4nm FinFET", 16, "DDR5-5600, LPDDR5X-7500, dual-channel, up to 96 GB DDR5 / 64 GB LPDDR5X", "2023-12-06",
    ("Radeon 780M", 12, "RDNA 3", 2700, None), "8840hs", "780m",
    "CPU and GPU: exact entries.",
    "AMD lists the NPU at up to 16 TOPS (39 TOPS overall).",
    [src("*", L + "8000-series/amd-ryzen-7-8840hs.html", "AMD spec page: CPU, memory, NPU and iGPU fields (no launch date)")]
    + pm_sources("8840hs", "780m")
    + [src("launch_date", TC + "ryzen-7-8840hs.c3401", "TPU: release Dec 6th, 2023"),
       tpu_gpu("radeon-780m.c4221", "8.294 TFLOPS (Hawk Point 780M; counts RDNA 3 dual-issue)")])

STRIX_DATE = ("AMD's page shows Launch Date 7/28/2025, which conflicts with TPU (Jul 2024) and PassMark "
              "(first seen Q3 2024); launch_date uses 2024-07.")
ROWS["ai9-hx370"] = row(
    "ai9-hx370", "AMD", "Ryzen AI 9 HX 370", "Strix Point", 12, 24, "4x Zen 5 + 8x Zen 5c", "Zen 5 / Zen 5c",
    2.0, 5.1, (28, 15, 54), 4, "TSMC 4nm FinFET", 50, "DDR5-5600, LPDDR5X-8000, dual-channel, up to 256 GB", "2024-07",
    ("Radeon 890M", 16, "RDNA 3.5", 2900, None), "hx370", "890m",
    "CPU and GPU: exact entries.",
    "Zen 5c cores run up to 3.3 GHz. " + STRIX_DATE,
    [src("*", L + "ai-300-series/amd-ryzen-ai-9-hx-370.html", "AMD spec page: CPU, memory, NPU and iGPU fields; its launch date 7/28/2025 is not used")]
    + pm_sources("hx370", "890m")
    + [src("launch_date", TC + "ryzen-ai-9-hx-370.c3655", "TPU: release Jul 2024"),
       tpu_gpu("radeon-890m.c4224", "5.939 TFLOPS")])

ROWS["ai9-365"] = row(
    "ai9-365", "AMD", "Ryzen AI 9 365", "Strix Point", 10, 20, "4x Zen 5 + 6x Zen 5c", "Zen 5 / Zen 5c",
    2.0, 5.0, (28, 15, 54), 4, "TSMC 4nm FinFET", 50, "DDR5-5600, LPDDR5X-8000, dual-channel, up to 256 GB", "2024-07",
    ("Radeon 880M", 12, "RDNA 3.5", 2900, None), "365", "880m",
    "CPU and GPU: exact entries.",
    "Zen 5c cores run up to 3.3 GHz. " + STRIX_DATE,
    [src("*", L + "ai-300-series/amd-ryzen-ai-9-365.html", "AMD spec page: CPU, memory, NPU and iGPU fields; its launch date 7/28/2025 is not used")]
    + pm_sources("365", "880m")
    + [src("launch_date", TC + "ryzen-ai-9-365.c3656", "TPU: release Jul 2024"),
       tpu_gpu("radeon-880m.c4225", "4.454 TFLOPS")])

HALO = "LPDDR5X-8000, 256-bit, up to 128 GB"
ROWS["ai-max-395"] = row(
    "ai-max-395", "AMD", "Ryzen AI Max+ 395", "Strix Halo", 16, 32, "16x Zen 5", "Zen 5", 3.0, 5.1, (55, 45, 120),
    4, "TSMC 4nm FinFET (CCDs and I/O die)", 50, HALO, "2025-01-06",
    ("Radeon 8060S", 40, "RDNA 3.5", 2900, None), "395", "8060s",
    "CPU and GPU: exact entries.",
    "Package with 3 dies (2 CCDs + I/O die).",
    [src("*", L + "ai-300-series/amd-ryzen-ai-max-plus-395.html", "AMD spec page: CPU, memory, NPU and iGPU fields (no launch date)")]
    + pm_sources("395", "8060s")
    + [src("launch_date", TC + "ryzen-ai-max-395.c3994", "TPU: release Jan 6th, 2025"),
       tpu_gpu("radeon-8060s.c4270", "14.85 TFLOPS")])

ROWS["ai-max-385"] = row(
    "ai-max-385", "AMD", "Ryzen AI Max 385", "Strix Halo", 8, 16, "8x Zen 5", "Zen 5", 3.6, 5.0, (55, 45, 120),
    4, "TSMC 4nm FinFET (CCD and I/O die)", 50, HALO, "2025-01-06",
    ("Radeon 8050S", 32, "RDNA 3.5", 2800, None), "385", "8050s",
    "CPU and GPU: exact entries (CPU has only 27 samples).",
    "Package with 2 dies (1 CCD + I/O die).",
    [src("*", L + "ai-300-series/amd-ryzen-ai-max-385.html", "AMD spec page: CPU, memory, NPU and iGPU fields (no launch date)")]
    + pm_sources("385", "8050s")
    + [src("launch_date", TC + "ryzen-ai-max-385.c3996", "TPU: release Jan 6th, 2025"),
       tpu_gpu("radeon-8050s.c4271", "11.47 TFLOPS")])

ROWS["ai-max-388"] = row(
    "ai-max-388", "AMD", "Ryzen AI Max+ 388", "Strix Halo", 8, 16, "8x Zen 5", "Zen 5", 3.6, 5.0, (55, 45, 120),
    4, "TSMC 4nm FinFET (CCD and I/O die)", 50, HALO, "2026-01-06",
    ("Radeon 8060S", 40, "RDNA 3.5", 2900, None), "388", "8060s",
    "CPU and GPU: exact entries (CPU entry 'AMD RYZEN AI MAX+ 388' has only 24 samples; the GPU entry pools all "
    "8060S hosts, mostly the 16-core 395).",
    "8 cores with the full 40 CU Radeon 8060S. PassMark first saw it in Q4 2025, before the TPU release date.",
    [src("*", L + "ai-300-series/amd-ryzen-ai-max-plus-388.html", "AMD spec page: CPU, memory, NPU and iGPU fields (no launch date)")]
    + pm_sources("388", "8060s")
    + [src("launch_date", TC + "ryzen-ai-max-388.c4312", "TPU: release Jan 6th, 2026"),
       tpu_gpu("radeon-8060s.c4270", "14.85 TFLOPS")])

# ---------- Intel ----------
ARK = "https://www.intel.com/content/www/us/en/products/sku/"
MTL_GPU = ("GPU: PassMark pools every 'Intel(R) Arc(TM) Graphics' iGPU (Meteor Lake and later H parts) under "
           "'Intel Arc'; there is no per-SKU entry.")
ROWS["cu5-135h"] = row(
    "cu5-135h", "Intel", "Core Ultra 5 135H", "Meteor Lake", 14, 18, "4P + 8E + 2LPE", "Redwood Cove + Crestmont",
    1.7, 4.6, (28, 20, 115), 4, "Intel 4 (compute tile, per ARK); TPU lists 7 nm", 11,
    "LPDDR5/X-7467, DDR5-5600, dual-channel, up to 96 GB", "2023-12-14",
    ("Intel Arc Graphics (8 Xe)", 8, "Xe-LPG", 2200, None), "135h", "arc",
    "CPU: exact entry. " + MTL_GPU,
    "base_ghz is the P-core base (E-core 1.2 GHz, LP E-core 0.7 GHz). igpu.name changed from the stub's '7 Xe': "
    "ARK lists 8 Xe-cores for the 135H (TPU's CPU page says 96 EU, its GPU page lists it under 128 EU). "
    "NPU 11 TOPS (33 TOPS overall). " + INTEL_TDP,
    [src("*", ARK + "236850/intel-core-ultra-5-processor-135h-18m-cache-up-to-4-60-ghz/specifications.html",
         "Intel ARK: cores, clocks, power, lithography, memory, Xe-cores, GPU clock, NPU")]
    + pm_sources("135h", "arc")
    + [src("launch_date", TC + "core-ultra-5-135h.c3419", "TPU: release Dec 14th, 2023 (ARK: Q4'23)"),
       src("cpu_arch", TC + "core-ultra-7-155h.c3307", "TPU: Redwood Cove P-cores, Crestmont E-cores and LP E-cores (Meteor Lake)"),
       tpu_gpu("arc-graphics-128eu-mobile.c4193", "4.608 TFLOPS (128 EU at 2250 MHz)")],
    fam="Intel")

ROWS["cu7-155h"] = row(
    "cu7-155h", "Intel", "Core Ultra 7 155H", "Meteor Lake", 16, 22, "6P + 8E + 2LPE", "Redwood Cove + Crestmont",
    1.4, 4.8, (28, 20, 115), 4, "Intel 4 (compute tile, per ARK); TPU lists 7 nm", 11,
    "LPDDR5/X-7467, DDR5-5600, dual-channel, up to 96 GB", "2023-12-14",
    ("Intel Arc Graphics (8 Xe)", 8, "Xe-LPG", 2250, None), "155h", "arc",
    "CPU: exact entry. " + MTL_GPU,
    "base_ghz is the P-core base (E-core 0.9 GHz, LP E-core 0.7 GHz). NPU 11 TOPS (33 TOPS overall). " + INTEL_TDP,
    [src("*", ARK + "236847/intel-core-ultra-7-processor-155h-24m-cache-up-to-4-80-ghz/specifications.html",
         "Intel ARK: cores, clocks, power, lithography, memory, Xe-cores, GPU clock, NPU")]
    + pm_sources("155h", "arc")
    + [src("launch_date", TC + "core-ultra-7-155h.c3307", "TPU: release Dec 14th, 2023 (ARK: Q4'23)"),
       src("cpu_arch", TC + "core-ultra-7-155h.c3307", "TPU: Redwood Cove P-cores, Crestmont E-cores and LP E-cores"),
       tpu_gpu("arc-graphics-128eu-mobile.c4193", "4.608 TFLOPS")],
    fam="Intel")

ROWS["cu7-258v"] = row(
    "cu7-258v", "Intel", "Core Ultra 7 258V", "Lunar Lake", 8, 8, "4P + 4LPE", "Lion Cove + Skymont",
    2.2, 4.8, (17, 8, 37), 3, "TSMC N3B (compute tile, per ARK)", 47,
    "LPDDR5X-8533 on-package, 32 GB", "2024-09-24",
    ("Intel Arc 140V", 8, "Xe2", 1950, None), "258v", "140v",
    "CPU and GPU: exact entries ('Intel Arc 140V GPU').",
    "No Hyper-Threading. NPU 47 TOPS (115 TOPS overall). " + INTEL_TDP,
    [src("*", ARK + "240957/intel-core-ultra-7-processor-258v-12m-cache-up-to-4-80-ghz/specifications.html",
         "Intel ARK: cores, clocks, power, lithography, memory, Xe-cores, GPU clock, NPU")]
    + pm_sources("258v", "140v")
    + [src("launch_date", TC + "core-ultra-7-258v.c3795", "TPU: release Sep 24th, 2024 (ARK: Q3'24)"),
       src("cpu_arch", TC + "core-ultra-7-258v.c3795", "TPU: Lion Cove P-cores, Skymont E-cores"),
       tpu_gpu("arc-140v-mobile.c4314", "3.994 TFLOPS")],
    fam="Intel")

ROWS["arc-g3-extreme"] = row(
    "arc-g3-extreme", "Intel", "Arc G3 Extreme", "Panther Lake", 14, 14, "2P + 8E + 4LPE", "Cougar Cove + Darkmont",
    1.9, 4.7, (25, 15, 80), 1.8, "Intel 18A (per ARK); TPU lists 3 nm", 46,
    "LPDDR5X-8533, dual-channel, up to 96 GB", "2026-05-28",
    ("Intel Arc B390", 12, "Xe3", 2300, None), "g3e", "b390",
    "CPU: exact entry 'Intel Arc G3 Extreme' (only 9 samples; PassMark's description says 'Intel Arc B380', "
    "but ARK names the iGPU Arc B390). GPU: 'Intel Arc B390 GPU' entry; most of its samples come from "
    "Panther Lake-H laptops (Core Ultra X7/X9) at higher power.",
    "Real SKU name of the stub 'Core Ultra / Arc G3 Extreme (handheld SKU)'; Intel brands it 'Intel Arc G3 Extreme "
    "Processor' (Arc G3 Processor Series). Used by the Acer Predator Atlas 8 and the MSI Claw 8 EX AI+. "
    "base_ghz is the P-core base (E-core and LP E-core 1.5 GHz). No Hyper-Threading. NPU 46 TOPS. "
    "launch_date from TPU; ARK says Q2'26. " + INTEL_TDP,
    [src("*", ARK + "245625/intel-arc-g3-extreme-processor-12m-cache-up-to-4-70-ghz/specifications.html",
         "Intel ARK: cores, clocks, power, Intel 18A, memory, Arc B390 GPU with 12 Xe-cores at 2.3 GHz, NPU 46 TOPS")]
    + pm_sources("g3e", "b390")
    + [src("name", "https://www.intel.com/content/www/us/en/products/details/processors/arc/g-series/handheld-gaming.html",
           "Intel Arc G-Series handheld page lists Arc G3 Extreme and Arc G3"),
       src("name", "https://retrohandhelds.gg/acer-predator-atlas-8-announced-at-computex-2026-powered-by-intel-arc-g3-extreme/",
           "Acer Predator Atlas 8 uses the Intel Arc G3 Extreme"),
       src("launch_date", TC + "arc-g3-extreme.c4437", "TPU: release May 28th, 2026"),
       src("cpu_arch", TC + "arc-g3-extreme.c4437", "TPU: Cougar Cove P-cores, Darkmont E-cores"),
       tpu_gpu("arc-g3-extreme.c4412", "7.680 TFLOPS (at 2500 MHz; ARK gives 2.3 GHz)")],
    fam="Intel")


# ---------- extra ids requested by the lead ----------
DRV = "https://www.amd.com/en/support/downloads/drivers.html/processors/ryzen/"
DRV_NOTE = "the AMD product page returns 404; this AMD driver page carries the full spec table"
CHIP_GPU = ("chip-named entry '{g}' (the iGPU reports as 'AMD Radeon Graphics'), chosen over the generic "
            "'{alt}' entry")

ROWS["r5-6600u"] = row(
    "r5-6600u", "AMD", "Ryzen 5 6600U", "Rembrandt", 6, 12, "6x Zen 3+", "Zen 3+", 2.9, 4.5, (15, 15, 28),
    6, "TSMC 6nm FinFET", 0, "DDR5-4800, LPDDR5-6400, dual-channel, up to 64 GB", "2022-04-19",
    ("Radeon 660M", 6, "RDNA 2", 1900, None), "6600u", "6600u",
    "CPU: exact entry (96 samples). GPU: " + CHIP_GPU.format(g="Radeon Ryzen 5 6600U", alt="Radeon 660M")
    + " (3197 G3D, only 13 samples).",
    "AMD gives only a 15-28 W cTDP; the 15 W default is from TPU. " + NPU0,
    [src("*", DRV + "ryzen-6000-series/amd-ryzen-5-6600u.html", DRV_NOTE)]
    + pm_sources("6600u", "6600u")
    + [src("tdp_w.default", TC + "ryzen-5-6600u.c2522", "TPU: TDP 15 W")])

ROWS["r5-5560u"] = row(
    "r5-5560u", "AMD", "Ryzen 5 5560U", "Cezanne", 6, 12, "6x Zen 3", "Zen 3", 2.3, 4.0, (15, 10, 25),
    7, "TSMC 7nm FinFET", 0, "DDR4-3200, LPDDR4X-4267, dual-channel, up to 64 GB", "2021-01-12",
    ("Radeon Vega 6", 6, "Vega (GCN 5)", 1600, None), "5560u", "5560u",
    "CPU: exact entry. GPU: chip-named entry 'Radeon Ryzen 5 5560U' (341 samples); the iGPU reports as "
    "'AMD Radeon Graphics' and PassMark's generic Vega 6 entries pool older chips.",
    "AMD names the iGPU only 'AMD Radeon Graphics' with 6 graphics cores; Vega 6 is the common name. "
    + NPU0,
    [src("*", DRV + "ryzen-5000-series/amd-ryzen-5-5560u.html", DRV_NOTE)]
    + pm_sources("5560u", "5560u"))

ROWS["r7-5825u"] = row(
    "r7-5825u", "AMD", "Ryzen 7 5825U", "Barcelo", 8, 16, "8x Zen 3", "Zen 3", 2.0, 4.5, (15, None, None),
    7, "TSMC 7nm FinFET", 0, "DDR4-3200, LPDDR4X-4267, dual-channel, up to 64 GB", "2022-01-30",
    ("Radeon Vega 8", 8, "Vega (GCN 5)", 2000, None), "5825u", "5825u",
    "CPU: exact entry. GPU: chip-named entry 'Radeon Ryzen 7 5825U' (2593 samples); the iGPU reports as "
    "'AMD Radeon Graphics'.",
    "Barcelo is a Cezanne refresh. AMD names the iGPU only 'AMD Radeon Graphics' with 8 graphics cores; TPU calls "
    "it Radeon Vega 8. AMD lists launch 01/30/2022; TPU lists Jan 6th, 2022. " + NPU0,
    [src("*", DRV + "ryzen-5000-series/amd-ryzen-7-5825u.html", DRV_NOTE)]
    + pm_sources("5825u", "5825u")
    + [src("igpu.name", TC + "ryzen-7-5825u.c2521", "TPU: Radeon Vega 8")],
)
ROWS["r7-5825u"]["unresolved"] = [
    {"field": "tdp_w.min", "reason": "AMD's spec table and TPU list only the 15 W default TDP, no cTDP range"},
    {"field": "tdp_w.max", "reason": "AMD's spec table and TPU list only the 15 W default TDP, no cTDP range"},
]

ROWS["r7-5800u"] = row(
    "r7-5800u", "AMD", "Ryzen 7 5800U", "Cezanne", 8, 16, "8x Zen 3", "Zen 3", 1.9, 4.4, (15, 10, 25),
    7, "TSMC 7nm FinFET", 0, "DDR4-3200, LPDDR4X-4266, dual-channel", "2021-01-12",
    ("Radeon Vega 8", 8, "Vega (GCN 5)", 2000, None), "5800u", "5800u",
    "CPU: exact entry. GPU: chip-named entry 'Radeon Ryzen 7 5800U' (708 samples); the iGPU reports as "
    "'AMD Radeon Graphics'.",
    "AMD names the iGPU only 'AMD Radeon Graphics' with 8 graphics cores; TPU calls it Radeon Vega 8. " + NPU0,
    [src("*", DRV + "ryzen-5000-series/amd-ryzen-7-5800u.html", DRV_NOTE)]
    + pm_sources("5800u", "5800u")
    + [src("cpu_arch", TC + "ryzen-7-5800u.c2746", "TPU: Zen 3 (Cezanne); AMD's table omits the architecture row"),
       src("igpu.name", TC + "ryzen-7-5800u.c2746", "TPU: Radeon Vega 8")])

ROWS["ai9-hx470"] = row(
    "ai9-hx470", "AMD", "Ryzen AI 9 HX 470", "Gorgon Point", 12, 24, "4x Zen 5 + 8x Zen 5c", "Zen 5 / Zen 5c",
    2.0, 5.2, (28, 15, 54), 4, "TSMC 4nm FinFET", 55, "DDR5-5600, LPDDR5X-8533, dual-channel, up to 256 GB",
    "2026-01-05", ("Radeon 890M", 16, "RDNA 3.5", 3100, None), "hx470", "890m",
    "CPU: exact entry (162 samples). GPU: 'Radeon 890M' entry; it pools all 890M hosts, mostly the HX 370 at "
    "2.9 GHz, so the HX 470's 3.1 GHz iGPU may score higher.",
    "Strix Point refresh (AMD codename Gorgon Point, Ryzen AI 400 series). AMD confirms the name and the Radeon 890M "
    "iGPU at 3.1 GHz. Zen 5c cores run up to 3.3 GHz. NPU 55 TOPS (86 TOPS overall).",
    [src("*", L + "ai-400-series/amd-ryzen-ai-9-hx-470.html", "AMD spec page: codename, CPU, memory, NPU, iGPU, launch 1/5/2026")]
    + pm_sources("hx470", "890m")
    + [src("process_nm", TC + "ryzen-ai-9-hx-470.c4320", "TPU: 4 nm, Gorgon Point, release Jan 2026")])

ROWS["r5-8640u"] = row(
    "r5-8640u", "AMD", "Ryzen 5 8640U", "Hawk Point", 6, 12, "6x Zen 4", "Zen 4", 3.5, 4.9, (28, 15, 30),
    4, "TSMC 4nm FinFET", 16, "DDR5-5600, LPDDR5X-7500, dual-channel, up to 96 GB DDR5 / 64 GB LPDDR5X", "2023-12-06",
    ("Radeon 760M", 8, "RDNA 3", 2600, None), "8640u", "760m",
    "CPU: exact entry 'AMD Ryzen 5 8640U' (44 samples). GPU: exact entry 'Radeon 760M'.",
    "AMD lists the NPU at up to 16 TOPS (31 TOPS overall).",
    [src("*", L + "8000-series/amd-ryzen-5-8640u.html", "AMD spec page: CPU, memory, NPU and iGPU fields (no launch date)")]
    + pm_sources("8640u", "760m")
    + [src("launch_date", TC + "ryzen-5-8640u.c3405", "TPU: release Dec 6th, 2023")])

ROWS["i7-1260p"] = row(
    "i7-1260p", "Intel", "Core i7-1260P", "Alder Lake-P", 12, 16, "4P + 8E", "Golden Cove + Gracemont",
    2.1, 4.7, (28, 20, 64), 7, "Intel 7 (per ARK); TPU lists 10 nm", 0,
    "DDR5-4800, DDR4-3200, LPDDR5-5200, LPDDR4X-4267, dual-channel, up to 64 GB", "2022-02-23",
    ("Intel Iris Xe (96 EU)", 6, "Xe-LP", 1400, None), "1260p", "irisxe",
    "CPU: exact entry. GPU: PassMark pools every 'Intel Iris Xe' iGPU (80 and 96 EU, many chips) under one entry; "
    "there is no per-SKU entry.",
    "igpu.cu counts the 96 EU as 6 subslices of 16 EU (the Xe-LP equivalent of an Xe-core). base_ghz is the P-core "
    "base from TPU (E-core 1.5 GHz). ARK lists no NPU, so npu_tops is 0. launch_date from TPU; ARK says Q1'22. "
    + INTEL_TDP,
    [src("*", ARK + "226254/intel-core-i71260p-processor-18m-cache-up-to-4-70-ghz/specifications.html",
         "Intel ARK: cores, turbo clocks, power, Intel 7, memory, Iris Xe 96 EU at 1.40 GHz")]
    + pm_sources("1260p", "irisxe")
    + [src("base_ghz", TC + "core-i7-1260p.c2581", "TPU: 2.1 GHz P-core base, 1.5 GHz E-core base"),
       src("launch_date", TC + "core-i7-1260p.c2581", "TPU: release Feb 23rd, 2022"),
       src("cpu_arch", "https://www.intel.com/content/www/us/en/developer/articles/guide/alder-lake-developer-guide.html",
           "Intel: Alder Lake P-cores are Golden Cove, E-cores are Gracemont")],
    fam="Intel")

ROWS["arc-g3"] = row(
    "arc-g3", "Intel", "Arc G3", "Panther Lake", 14, 14, "2P + 8E + 4LPE", "Cougar Cove + Darkmont",
    1.9, 4.6, (25, 15, 80), 1.8, "Intel 18A (per ARK); TPU lists 3 nm", 46,
    "LPDDR5X-8533, dual-channel, up to 96 GB", "2026-05-28",
    ("Intel Arc B370", 10, "Xe3", 2200, None), "g3e", "b370",
    "CPU: PassMark has no 'Intel Arc G3' entry; stand-in = 'Intel Arc G3 Extreme' (same 2P + 8E + 4LPE die and "
    "25 W base power; the G3 boosts to 4.6 GHz instead of 4.7 GHz). GPU: 'Intel Arc B370 GPU' entry (57 samples, "
    "mostly Panther Lake-H laptops at higher power).",
    "Intel brands it 'Intel Arc G3 Processor' (processor number G3); no Core Ultra model number. Used by the MSI "
    "Claw 8 EX AI+ (CG3M). base_ghz is the P-core base (E-core and LP E-core 1.5 GHz). No Hyper-Threading. "
    "NPU 46 TOPS. launch_date from TPU; ARK says Q2'26. " + INTEL_TDP,
    [src("*", ARK + "245626/intel-arc-g3-processor-12m-cache-up-to-4-60-ghz/specifications.html",
         "Intel ARK: cores, clocks, power, Intel 18A, memory, Arc B370 GPU with 10 Xe-cores at 2.2 GHz, NPU 46 TOPS")]
    + pm_sources("g3e", "b370")
    + [src("launch_date", TC + "arc-g3.c4436", "TPU: release May 28th, 2026"),
       src("cpu_arch", TC + "arc-g3.c4436", "TPU: Cougar Cove P-cores, Darkmont E-cores")],
    fam="Intel")


# ---------- OneXPlayer crawler ids ----------
IRIS_GPU = ("GPU: PassMark pools every 'Intel Iris Xe' iGPU (80 and 96 EU, many chips) under one entry; "
            "there is no per-SKU entry.")
IRIS_CU = "igpu.cu counts the 96 EU as 6 subslices of 16 EU (the Xe-LP equivalent of an Xe-core). "

ROWS["cu7-255h"] = row(
    "cu7-255h", "Intel", "Core Ultra 7 255H", "Arrow Lake-H", 16, 16, "6P + 8E + 2LPE", "Lion Cove + Skymont",
    2.0, 5.1, (28, 20, 115), 3, "TSMC N3B (compute tile, per ARK)", 13,
    "LPDDR5/X-8400, DDR5-6400, dual-channel, up to 128 GB", "2025-01-13",
    ("Intel Arc 140T", 8, "Xe-LPG+", 2250, None), "255h", "140t",
    "CPU and GPU: exact entries ('Intel Arc 140T GPU', 2295 samples).",
    "base_ghz is the P-core base (E-core 1.5 GHz). No Hyper-Threading. NPU 13 TOPS (96 TOPS overall). "
    "launch_date from TPU; ARK says Q1'25. " + INTEL_TDP,
    [src("*", ARK + "241751/intel-core-ultra-7-processor-255h-24m-cache-up-to-5-10-ghz/specifications.html",
         "Intel ARK: cores, clocks, power, TSMC N3B, memory, Arc 140T with 8 Xe-cores at 2.25 GHz, NPU")]
    + pm_sources("255h", "140t")
    + [src("launch_date", TC + "core-ultra-7-255h.c4268", "TPU: release Jan 13th, 2025"),
       src("cpu_arch", TC + "core-ultra-7-255h.c4268", "TPU: Lion Cove P-cores, Skymont E-cores"),
       src("igpu.arch", TG + "arc-140t-mobile.c4268", "TPU: Xe-LPG+"),
       tpu_gpu("arc-140t-mobile.c4268", "4.813 TFLOPS (at 2350 MHz; ARK gives 2.25 GHz for the 255H)")],
    fam="Intel")

ROWS["cu5-125h"] = row(
    "cu5-125h", "Intel", "Core Ultra 5 125H", "Meteor Lake", 14, 18, "4P + 8E + 2LPE", "Redwood Cove + Crestmont",
    1.2, 4.5, (28, 20, 115), 4, "Intel 4 (compute tile, per ARK); TPU lists 7 nm", 11,
    "LPDDR5/X-7467, DDR5-5600, dual-channel, up to 96 GB", "2023-12-14",
    ("Intel Arc Graphics (7 Xe)", 7, "Xe-LPG", 2200, None), "125h", "arc",
    "CPU: exact entry. " + MTL_GPU,
    "base_ghz is the P-core base. ARK lists 7 Xe-cores (the 135H has 8). NPU 11 TOPS (33 TOPS overall). "
    "launch_date from TPU; ARK says Q4'23. " + INTEL_TDP,
    [src("*", ARK + "236848/intel-core-ultra-5-processor-125h-18m-cache-up-to-4-50-ghz/specifications.html",
         "Intel ARK: cores, clocks, power, lithography, memory, 7 Xe-cores at 2.2 GHz, NPU")]
    + pm_sources("125h", "arc")
    + [src("launch_date", TC + "core-ultra-5-125h.c3309", "TPU: release Dec 14th, 2023"),
       src("cpu_arch", TC + "core-ultra-5-125h.c3309", "TPU: Redwood Cove P-cores, Crestmont E-cores"),
       tpu_gpu("arc-graphics-112eu-mobile.c4196", "3.942 TFLOPS")],
    fam="Intel")

ROWS["cu5-228v"] = row(
    "cu5-228v", "Intel", "Core Ultra 5 228V", "Lunar Lake", 8, 8, "4P + 4LPE", "Lion Cove + Skymont",
    2.1, 4.5, (17, 8, 37), 3, "TSMC N3B (compute tile, per ARK)", 40,
    "LPDDR5X-8533 on-package, 32 GB", "2024-09-24",
    ("Intel Arc 130V", 7, "Xe2", 1850, None), "228v", "130v",
    "CPU and GPU: exact entries ('Intel Arc 130V GPU', 1456 samples).",
    "No Hyper-Threading. NPU 40 TOPS (97 TOPS overall). launch_date from TPU; ARK says Q3'24. " + INTEL_TDP,
    [src("*", ARK + "240955/intel-core-ultra-5-processor-228v-8m-cache-up-to-4-50-ghz/specifications.html",
         "Intel ARK: cores, clocks, power, TSMC N3B, memory, Arc 130V with 7 Xe-cores at 1.85 GHz, NPU")]
    + pm_sources("228v", "130v")
    + [src("launch_date", TC + "core-ultra-5-228v.c3799", "TPU: release Sep 24th, 2024"),
       src("cpu_arch", TC + "core-ultra-5-228v.c3799", "TPU: Lion Cove P-cores, Skymont E-cores"),
       tpu_gpu("arc-130v-mobile.c4315", "3.315 TFLOPS")],
    fam="Intel")

ROWS["i7-1360p"] = row(
    "i7-1360p", "Intel", "Core i7-1360P", "Raptor Lake-P", 12, 16, "4P + 8E", "Raptor Cove + Gracemont",
    2.2, 5.0, (28, 20, 64), 7, "Intel 7 (per ARK); TPU lists 10 nm", 0,
    "DDR5-5200, DDR4-3200, LPDDR5/X-6400, LPDDR4X-4267, dual-channel, up to 96 GB", "2023-01-04",
    ("Intel Iris Xe (96 EU)", 6, "Xe-LP", 1500, None), "1360p", "irisxe",
    "CPU: exact entry. " + IRIS_GPU,
    IRIS_CU + "base_ghz is the P-core base from TPU (E-core 1.6 GHz). ARK lists no NPU, so npu_tops is 0. "
    "launch_date from TPU; ARK says Q1'23. " + INTEL_TDP,
    [src("*", ARK + "232155/intel-core-i71360p-processor-18m-cache-up-to-5-00-ghz/specifications.html",
         "Intel ARK: cores, turbo clock, power, Intel 7, memory, Iris Xe 96 EU at 1.50 GHz")]
    + pm_sources("1360p", "irisxe")
    + [src("base_ghz", TC + "core-i7-1360p.c3059", "TPU: 2.2 GHz P-core base, 1.6 GHz E-core base"),
       src("launch_date", TC + "core-i7-1360p.c3059", "TPU: release Jan 4th, 2023"),
       src("cpu_arch", "https://download.intel.com/newsroom/2022/2022innovation/13th-Gen-Intel-Core-Desktop-Media-presentation.pdf",
           "Intel names the 13th Gen P-core Raptor Cove; the E-core is Gracemont, carried over from Alder Lake")],
    fam="Intel")

ROWS["i7-1195g7"] = row(
    "i7-1195g7", "Intel", "Core i7-1195G7", "Tiger Lake", 4, 8, "4x Willow Cove", "Willow Cove",
    2.9, 5.0, (28, 12, 28), 10, "Intel 10 nm SuperFin (per ARK)", 0,
    "DDR4-3200, LPDDR4X-4267, dual-channel, up to 64 GB", "2021-05-31",
    ("Intel Iris Xe (96 EU)", 6, "Xe-LP", 1400, None), "1195g7", "irisxe",
    "CPU: exact entry 'Intel Core i7-1195G7 @ 2.90GHz'. " + IRIS_GPU,
    IRIS_CU + "Tiger Lake has no hybrid cores and no NPU (ARK lists none; the 'with IPU' SKU name refers to the "
    "image processing unit). tdp_w: default 28 W from TPU; min and max are ARK's cTDP-down 12 W and cTDP-up 28 W. "
    "base_ghz is the 28 W base from TPU. launch_date from TPU; ARK says Q2'21.",
    [src("*", ARK + "217181/intel-core-i71195g7-processor-12m-cache-up-to-5-00-ghz-with-ipu/specifications.html",
         "Intel ARK: cores, turbo clock, cTDP 12-28 W, 10 nm SuperFin, memory, Iris Xe 96 EU at 1.40 GHz")]
    + pm_sources("1195g7", "irisxe")
    + [src("base_ghz", TC + "core-i7-1195g7.c4212", "TPU: 2.9 GHz base, TDP 28 W"),
       src("launch_date", TC + "core-i7-1195g7.c4212", "TPU: release May 31st, 2021"),
       src("cpu_arch", "https://download.intel.com/newsroom/2020/client-computing/intel-2020-architecture-day-fact-sheet.pdf",
           "Intel Architecture Day 2020: Tiger Lake uses Willow Cove cores")],
    fam="Intel")


def main(argv):
    outdir = pathlib.Path(argv[0])
    for id_, data in ROWS.items():
        path = outdir / f"{id_}.json"
        if path.exists():
            stub = json.loads(path.read_text())
            assert stub["id"] == id_, (stub["id"], id_)
        # Drop null source notes to keep files tidy.
        for s in data["sources"]:
            if s.get("note") is None:
                s.pop("note", None)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print("wrote", path.name)


if __name__ == "__main__":
    main(sys.argv[1:])
