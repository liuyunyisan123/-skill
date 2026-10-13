#!/usr/bin/env python3
"""Check EMF records for bitmap content without assuming that vector paths prove purity.

Uses the Python standard library. Does not validate rendering or Office editability.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import sys

BITMAP_RECORDS = {
    76: "EMR_BITBLT", 77: "EMR_STRETCHBLT", 78: "EMR_MASKBLT",
    79: "EMR_PLGBLT", 80: "EMR_SETDIBITSTODEVICE", 81: "EMR_STRETCHDIBITS",
    93: "EMR_CREATEMONOBRUSH", 94: "EMR_CREATEDIBPATTERNBRUSHPT",
    114: "EMR_ALPHABLEND", 116: "EMR_TRANSPARENTBLT",
}
PATH_RECORDS = {2, 3, 4, 5, 6, 7, 42, 43, 44, 45, 46, 47,
                54, 59, 60, 62, 63, 64, 85, 86, 87, 88, 89, 90, 91, 92}
TEXT_RECORDS = {83, 84, 96, 97, 108}


def u32(data, offset):
    return struct.unpack_from("<I", data, offset)[0]


def parse_emfplus(record, problems):
    """Recognize EMF+ image objects; unproven embedded metafiles stay flagged."""
    if len(record) < 12:
        raise ValueError("Truncated GDI comment")
    count = u32(record, 8)
    if 12 + count > len(record):
        raise ValueError("Invalid GDI comment length")
    payload = record[12:12 + count]
    if payload[:4] != b"EMF+":
        return {"unknown_comments": 1 if count else 0, "bitmap_images": 0,
                "image_objects": 0, "records": 0, "text_records": 0}
    result = {"unknown_comments": 0, "bitmap_images": 0,
              "image_objects": 0, "records": 0, "text_records": 0}
    position = 4
    while position < len(payload):
        if len(payload) - position < 12:
            raise ValueError("Truncated EMF+ record")
        kind, flags, size, data_size = struct.unpack_from("<HHII", payload, position)
        if size < 12 or size % 4 or position + size > len(payload) or data_size > size - 12:
            raise ValueError("Invalid EMF+ record boundary")
        result["records"] += 1
        if kind in (0x401C, 0x4036):
            result["text_records"] += 1
        if kind == 0x4008 and ((flags >> 8) & 0x7F) == 5:
            result["image_objects"] += 1
            if not flags & 0x8000 and data_size >= 8:
                image_type = u32(payload, position + 16)
                if image_type == 1:
                    result["bitmap_images"] += 1
                elif image_type == 2:
                    problems.add("EMF+ embedded metafile image requires payload inspection")
                else:
                    problems.add("Unknown EMF+ image type")
            else:
                problems.add("Continued or truncated EMF+ image object requires inspection")
        position += size
    return result


def audit(path):
    data = path.read_bytes()
    if len(data) < 88 or u32(data, 0) != 1 or u32(data, 40) != 0x464D4520:
        raise ValueError("Not a valid classic EMF header; extension alone is insufficient")
    if u32(data, 4) < 88 or u32(data, 48) != len(data):
        raise ValueError("EMF header size or declared file length does not match")
    counts = Counter()
    fonts = []
    problems = set()
    plus = Counter()
    bitmap_pens = 0
    position = 0
    last_kind = None
    while position < len(data):
        if len(data) - position < 8:
            raise ValueError("Truncated EMF record header")
        kind, size = struct.unpack_from("<II", data, position)
        if size < 8 or size % 4 or position + size > len(data):
            raise ValueError(f"Invalid record boundary at byte {position}")
        record = data[position:position + size]
        counts[kind] += 1
        if kind < 1 or kind > 122:
            problems.add("Unknown classic EMF record type requires inspection")
        if kind == 70:
            plus.update(parse_emfplus(record, problems))
        elif kind == 95:
            if size < 52:
                raise ValueError("Truncated extended pen record")
            if u32(record, 16) or u32(record, 24) or u32(record, 36) in (3, 5, 6, 7, 8, 9):
                bitmap_pens += 1
        elif kind == 82:
            if size < 104:
                raise ValueError("Truncated Unicode font record")
            face = record[40:104].decode("utf-16le").split("\0", 1)[0]
            fonts.append({"face": face, "italic": bool(record[32]),
                          "charset": record[35]})
        elif kind == 84:
            if size < 76:
                raise ValueError("Truncated Unicode text record")
            length, offset = struct.unpack_from("<II", record, 44)
            if length and (offset < 76 or offset + length * 2 > size):
                raise ValueError("Unicode text falls outside its record")
            options = u32(record, 52)
            # ETO_GLYPH_INDEX stores glyph identifiers rather than Unicode strings.
            if length and not options & 0x10:
                record[offset:offset + length * 2].decode("utf-16le")
        position += size
        last_kind = kind
    if last_kind != 14 or sum(counts.values()) != u32(data, 52):
        raise ValueError("EOF or declared EMF record count does not match")
    bitmaps = {BITMAP_RECORDS[k]: counts[k] for k in BITMAP_RECORDS if counts[k]}
    if bitmap_pens:
        bitmaps["EMR_EXTCREATEPEN_BITMAP_BRUSH"] = bitmap_pens
    if bitmaps:
        problems.add("Classic bitmap operation or bitmap brush found")
    if plus["bitmap_images"]:
        problems.add("EMF+ bitmap image object found")
    if plus["records"]:
        # Texture brushes and other nested EMF+ resources can carry image data.
        # This lightweight parser does not prove the purity of every such payload.
        problems.add("EMF+ nested resources require complete payload inspection")
    if plus["unknown_comments"]:
        problems.add("GDI comment payload requires inspection")
    if counts[15]:
        problems.add("EMR_SETPIXELV found; inspect pixel drawing")
    if any(counts[k] for k in (102, 103, 105, 106, 110)):
        problems.add("OpenGL or escape payload requires inspection")
    if plus["image_objects"] and not plus["bitmap_images"]:
        problems.add("EMF+ image-object vector purity is unproven")
    return {
        "file": str(path.resolve()), "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "header_and_record_boundaries_valid": True,
        "record_counts": dict(sorted(counts.items())),
        "classic_bitmap_operations": bitmaps,
        "classic_bitmap_record_count": sum(bitmaps.values()),
        "emfplus_record_count": plus["records"],
        "emfplus_image_object_count": plus["image_objects"],
        "emfplus_bitmap_image_count": plus["bitmap_images"],
        "unknown_GDI_comment_count": plus["unknown_comments"],
        "path_or_geometry_record_count": sum(counts[k] for k in PATH_RECORDS),
        "text_record_count": sum(counts[k] for k in TEXT_RECORDS) + plus["text_records"],
        "italic_font_records": sum(f["italic"] for f in fonts),
        "font_faces": sorted({f["face"] for f in fonts}),
        "font_charsets": sorted({f["charset"] for f in fonts}),
        "pure_vector_record_check": not problems,
        "issues_requiring_attention": sorted(problems),
        "rendering_verified": False,
        "PowerPoint_editability_verified": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="EMF files or directories")
    parser.add_argument("--out", type=Path, help="Write UTF-8 JSON report")
    parser.add_argument("--require-pure-vector", action="store_true",
                        help="Fail if bitmap records or unproven payloads are found")
    args = parser.parse_args()
    paths = []
    for path in args.paths:
        paths.extend(sorted(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() == ".emf")
                     if path.is_dir() else [path])
    paths = list(dict.fromkeys(paths))
    if not paths:
        parser.error("No EMF files found")
    reports = []
    invalid = False
    for path in paths:
        try:
            report = audit(path)
        except (OSError, ValueError, struct.error, UnicodeError) as error:
            invalid = True
            report = {"file": str(path.resolve()), "header_and_record_boundaries_valid": False,
                      "pure_vector_record_check": False, "error": str(error)}
        reports.append(report)
    result = {"files": reports,
              "scope": "Record structure only; rendering, fonts and Office editability need separate checks."}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output + "\n", encoding="utf-8")
        print(f"Checked {len(reports)} file(s); report: {args.out}")
    else:
        print(output)
    if invalid:
        return 1
    if args.require_pure_vector and any(not r["pure_vector_record_check"] for r in reports):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
