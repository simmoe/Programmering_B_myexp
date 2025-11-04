#!/usr/bin/env python3
import os, re, sys, pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"
START = "<!-- AUTO-INDEX:START -->"
END   = "<!-- AUTO-INDEX:END -->"

# Konfiguration
IGNORE_DIRS = {".git", ".github", "node_modules", "__pycache__", ".venv", "venv", ".vscode", "dist", "build"}

def first_heading_of(subdir: pathlib.Path):
    # Læs første linje i README.* i undermappen, hvis den findes, og brug som kort beskrivelse
    for name in ("README.md", "Readme.md", "readme.md", "README"):
        p = subdir / name
        if p.is_file():
            with p.open(encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line=line.strip()
                    if line and not line.startswith("<!") and not line.startswith("[!") and not line.startswith("# ") and not line.startswith("---"):
                        return line[:140]
            break
    return ""

def generate_index():
    items = []
    for entry in sorted(os.listdir(REPO_ROOT)):
        p = REPO_ROOT / entry
        if p.is_dir() and entry not in IGNORE_DIRS and not entry.startswith(".") and not entry.startswith("_"):
            desc = first_heading_of(p)
            if desc:
                items.append(f"- [{entry}](./{entry}/) – {desc}")
            else:
                items.append(f"- [{entry}](./{entry}/)")
    if not items:
        items.append("_Ingen undermapper fundet_")
    return "\n".join(items)

def main():
    md = README.read_text(encoding="utf-8")
    if START not in md or END not in md:
        # Hvis markører ikke findes, tilføj dem i bunden
        md = md.rstrip() + f"\n\n{START}\n{END}\n"

    block = generate_index()
    new_md = re.sub(rf"{re.escape(START)}.*?{re.escape(END)}", f"{START}\n{block}\n{END}", md, flags=re.S)
    if new_md != md:
        README.write_text(new_md, encoding="utf-8")
        print("README opdateret")
    else:
        print("Ingen ændringer")

if __name__ == "__main__":
    sys.exit(main())
