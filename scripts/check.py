# /// script
# requires-python = ">=3.11"
# dependencies = ["queria"]
# ///
"""語彙の約束を確かめる。

    uv run scripts/check.py

GIF と schema.org の語は Queria の公開データセット（gif・schemaorg）から引く。

- entities.csv の name は重複しないこと
- data_elements.csv の entity は entities.csv にある名前であること
- gif_term は gif.vocab.term の同じ class にある語であること
- schema_org は schemaorg.vocab.property にある語であること
- 語彙の語がある行の name は、GIF か schema.org の語を snake_case にしたものであること
- データ項目の name と aliases はそれぞれ重複せず、互いに重ならないこと
"""

import csv
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(name: str) -> list[dict]:
    with (ROOT / name).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def snake(term: str) -> str:
    # gif.vocab.term・schemaorg.vocab.property の snake_case_name と同じ規則（height_CMT → height_cmt）
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", term).lower()


def candidates(e: dict) -> set[str]:
    return {snake(t) for t in (e["gif_term"], e["schema_org"]) if t}


def duplicates(values: list[str]) -> list[str]:
    return sorted({v for v in values if values.count(v) > 1})


def problems(entities: list[dict], elements: list[dict], gif: set[tuple[str, str]], schemaorg: set[str]) -> list[str]:
    entity_names = [e["name"] for e in entities]
    names = [e["name"] for e in elements]
    aliases = [a for e in elements for a in e["aliases"].split(";") if a]
    return [
        *(f"{n}: entity が重複している" for n in duplicates(entity_names)),
        *(f"{e['name']}: entity の {e['entity']} が entities.csv に無い" for e in elements if e["entity"] and e["entity"] not in entity_names),
        *(f"{e['name']}: GIF の {e['gif_class']} に {e['gif_term']} が無い" for e in elements if e["gif_term"] and (e["gif_class"], e["gif_term"]) not in gif),
        *(f"{e['name']}: schema.org に {e['schema_org']} が無い" for e in elements if e["schema_org"] and e["schema_org"] not in schemaorg),
        *(f"{e['name']}: {' か '.join(sorted(candidates(e)))} にする" for e in elements if candidates(e) and e["name"] not in candidates(e)),
        *(f"{n}: データ項目が重複している" for n in duplicates(names)),
        *(f"{a}: alias が重複している" for a in duplicates(aliases)),
        *(f"{a}: alias がデータ項目の name と重なっている" for a in sorted(set(aliases) & set(names))),
    ]


def vocabularies() -> tuple[set[tuple[str, str]], set[str]]:
    import queria

    con = queria.connect(token=os.environ.get("QUERIA_TOKEN") or None)
    gif = {tuple(r) for r in con.sql("SELECT class_name, term_en FROM gif.vocab.term").fetchall()}
    schemaorg = {r[0] for r in con.sql("SELECT name FROM schemaorg.vocab.property").fetchall()}
    return gif, schemaorg


if __name__ == "__main__":
    found = problems(read("entities.csv"), read("data_elements.csv"), *vocabularies())
    print("\n".join(found) or "ok", file=sys.stderr)
    sys.exit(1 if found else 0)
