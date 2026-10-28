#!/usr/bin/env python3
"""Inventario estatico de IPA/TIPA, somente leitura. Nunca instala ou executa o alvo."""

import argparse
import hashlib
import json
import pathlib
import plistlib
import sys
import zipfile

CHUNK = 1024 * 1024
MAX_ENTRIES = 20000
MAX_UNCOMPRESSED = 4 * 1024**3
PLIST_MAX = 1024 * 1024
PLIST_KEYS = (
    "CFBundleIdentifier", "CFBundleName", "CFBundleExecutable",
    "CFBundleVersion", "CFBundleShortVersionString", "MinimumOSVersion",
    "LSMinimumSystemVersion", "UIDeviceFamily", "UIRequiredDeviceCapabilities",
)


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def scan(path):
    path = pathlib.Path(path).expanduser().resolve(strict=True)
    if not path.is_file() or not zipfile.is_zipfile(path):
        raise ValueError("O ficheiro nao e um IPA/TIPA (arquivo ZIP) valido")

    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        if len(infos) > MAX_ENTRIES:
            raise ValueError("Arquivo com demasiadas entradas")
        if sum(entry.file_size for entry in infos) > MAX_UNCOMPRESSED:
            raise ValueError("Arquivo expandido excede o limite de seguranca")
        entries = []
        app_metadata = []
        for entry in infos:
            if entry.is_dir():
                continue
            digest = hashlib.sha256()
            with archive.open(entry) as source:
                for block in iter(lambda: source.read(CHUNK), b""):
                    digest.update(block)
            item = {
                "path": entry.filename,
                "size": entry.file_size,
                "sha256": digest.hexdigest(),
            }
            entries.append(item)
            parts = entry.filename.split("/")
            if (len(parts) == 3 and parts[0] == "Payload"
                    and parts[1].endswith(".app") and parts[2] == "Info.plist"):
                meta = {"path": entry.filename}
                if entry.file_size <= PLIST_MAX:
                    try:
                        with archive.open(entry) as stream:
                            plist = plistlib.loads(stream.read())
                        if isinstance(plist, dict):
                            meta["properties"] = {
                                key: plist[key] for key in PLIST_KEYS if key in plist
                            }
                    except (ValueError, TypeError, plistlib.InvalidFileException) as exc:
                        meta["parse_error"] = str(exc)
                else:
                    meta["parse_error"] = "Info.plist demasiado grande"
                app_metadata.append(meta)

    names = [item["path"] for item in entries]
    notable = [name for name in names if (
        name.lower().endswith((".deb", ".dylib", ".framework", ".appex", ".tipa"))
        or ".framework/" in name.lower()
        or any(term in name.lower() for term in ("roothide", "patcher", "sileo", "vcam"))
    )]
    return {
        "schema": 1,
        "file_name": path.name,
        "archive_bytes": path.stat().st_size,
        "archive_sha256": sha256_file(path),
        "entry_count": len(entries),
        "apps": app_metadata,
        "notable_paths": notable,
        "entries": entries,
        "observations": [
            "Inventario estatico; nao comprova suporte iOS, jailbreak nem funcionamento de tweaks.",
            "Ausencia de palavra no nome do ficheiro nao comprova ausencia de funcionalidade.",
        ],
    }


def compare(original, candidate):
    old = {item["path"]: item["sha256"] for item in original["entries"]}
    new = {item["path"]: item["sha256"] for item in candidate["entries"]}
    return {
        "missing": sorted(old.keys() - new.keys()),
        "added": sorted(new.keys() - old.keys()),
        "changed": sorted(name for name in old.keys() & new.keys() if old[name] != new[name]),
        "unchanged_count": sum(old[name] == new[name] for name in old.keys() & new.keys()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ipa", help="IPA/TIPA original ou versao candidata")
    parser.add_argument("--output", required=True, help="Caminho do JSON de saida")
    parser.add_argument("--compare", help="JSON de inventario original, para comparar com o candidato")
    args = parser.parse_args()
    try:
        result = scan(args.ipa)
        if args.compare:
            with pathlib.Path(args.compare).open(encoding="utf-8") as stream:
                original = json.load(stream)
            result["comparison_with_original"] = compare(original, result)
        output = pathlib.Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"SHA-256: {result['archive_sha256']}")
        print(f"Ficheiros: {result['entry_count']}; relatorio: {output}")
        if args.compare:
            delta = result["comparison_with_original"]
            print("Comparacao: " + ", ".join(f"{k}={len(v) if isinstance(v, list) else v}" for k, v in delta.items()))
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError, KeyError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
