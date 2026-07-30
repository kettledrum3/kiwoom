with open("API_SPEC.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

start = -1
for idx, line in enumerate(lines):
    if "## [00]" in line:
        start = idx
        break

if start != -1:
    for idx in range(start, start + 30):
        if idx < len(lines):
            # remove non-ascii for safe printing
            clean_line = lines[idx].encode('ascii', errors='ignore').decode('ascii').strip()
            print(f"Line {idx+1}: {clean_line}")
