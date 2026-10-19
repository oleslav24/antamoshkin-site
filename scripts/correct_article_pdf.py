"""Correct publisher placeholders while retaining embedded fonts and text positions."""
from pathlib import Path
import re

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ByteStringObject, TextStringObject


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("C:/Users/oanta/YandexDisk/Articles/2026/Мультиагентная система/ПИ/принято в печать/жучков.pdf")
TARGET = ROOT / "public/papers/llm-agent-fitness-2026.pdf"


def font_mapping(font):
    cmap = font.get_object()["/ToUnicode"].get_object().get_data().decode("ascii")
    mapping = {}
    for block in re.findall(r"beginbfchar(.*?)endbfchar", cmap, re.S):
        for key, value in re.findall(r"<([\da-f]+)>\s*<([\da-f]+)>", block, re.I):
            mapping[int(key, 16)] = bytes.fromhex(value).decode("utf-16-be")
    for block in re.findall(r"beginbfrange(.*?)endbfrange", cmap, re.S):
        for start, end, value in re.findall(r"<([\da-f]+)>\s*<([\da-f]+)>\s*<([\da-f]+)>", block, re.I):
            for key in range(int(start, 16), int(end, 16) + 1):
                mapping[key] = chr(int(value, 16) + key - int(start, 16))
    return mapping


reader = PdfReader(SOURCE)
writer = PdfWriter()
writer.clone_document_from_reader(reader)
changes = 0
for page in writer.pages:
    maps = {key: font_mapping(font) for key, font in page["/Resources"]["/Font"].items()}
    font = None
    content = page.get_contents()
    for operands, operator in content.operations:
        if operator == b"Tf":
            font = operands[0]
        if operator not in (b"TJ", b"Tj"):
            continue
        strings = operands[0] if operator == b"TJ" else operands
        mapping = maps[font]
        reverse = {value: key for key, value in mapping.items()}
        segments = []
        for index, item in enumerate(strings):
            if isinstance(item, (TextStringObject, ByteStringObject)):
                raw = item.get_original_bytes() if isinstance(item, TextStringObject) else bytes(item)
                segments.append((index, "".join(mapping.get(char, chr(char)) for char in raw)))
        combined = "".join(value for _, value in segments)
        replacements = []
        if "000" in combined and ("535" in combined or "DOI" in combined):
            start = combined.index("000")
            replacements.append((start, start + 3, "541"))
        if "10.17587/prin.535-541" in combined:
            start = combined.index("prin.535-541") + len("prin.")
            replacements.append((start, start, "17."))
        for start, end, replacement in replacements:
            offset = 0
            for index, value in segments:
                limit = offset + len(value)
                if offset <= start < limit or start < limit and end > offset:
                    prefix = value[:max(0, start-offset)]
                    suffix = value[min(len(value), max(0, end-offset)):]
                    value = prefix + (replacement if offset <= start < limit else "") + suffix
                    strings[index] = ByteStringObject(bytes(reverse[char] for char in value))
                    if offset <= start < limit:
                        changes += 1
                offset = limit
    page.replace_contents(content)
if changes != 4:
    raise ValueError(f"Expected four corrections, got {changes}")
writer.write(TARGET)
print(f"Corrected {changes} occurrences: {TARGET}")
