#!/usr/bin/env python3
"""Call the reviewed Imrane installer, exposing skills at governance only.

Compatibility entrypoint: the core installer itself uses governance-only exposure.
The real registry and existing business-lane skill folders are unchanged.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / 'systeme-imrane/scripts'))
import skills

if __name__ == '__main__':
    sys.exit(skills.main())
