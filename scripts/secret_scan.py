from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
SKIP = {".git", ".venv", ".terraform", "__pycache__"}
PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github token": re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    "aws access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "assigned secret": re.compile(
        r"(?i)(?:api[_-]?key|password|client[_-]?secret)\s*[=:]\s*['\"][^'\"]{12,}['\"]"
    ),
}

findings: list[str] = []
for path in ROOT.rglob("*"):
    if not path.is_file() or any(part in SKIP for part in path.parts):
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    if path.name == ".env.example":
        continue
    for label, pattern in PATTERNS.items():
        if pattern.search(text):
            findings.append(f"{path.relative_to(ROOT)}: {label}")

if findings:
    print("Potential secrets detected:")
    print("\n".join(findings))
    sys.exit(1)
print("Secret scan passed")
