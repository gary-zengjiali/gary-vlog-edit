#!/usr/bin/env python3
"""Validate this portable editing skill without needing local video projects."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import subprocess
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
MEDIA = {'.mp4', '.mov', '.m4v', '.mkv', '.avi', '.wav', '.mp3', '.m4a',
         '.aac', '.flac', '.heic', '.jpg', '.jpeg', '.png', '.cube', '.fcpxml'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def source_files():
    if (ROOT / '.git').exists():
        result = subprocess.check_output(
            ['git', '-C', str(ROOT), 'ls-files', '-z'])
        return [ROOT / s.decode() for s in result.split(b'\0') if s]
    return [p for p in ROOT.rglob('*') if p.is_file()
            and not any(part.startswith('.') or part == '__pycache__'
                        for part in p.relative_to(ROOT).parts)]


def main():
    text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    require(match is not None, 'SKILL.md needs YAML frontmatter')
    meta = yaml.safe_load(match.group(1))
    require(isinstance(meta, dict), 'Frontmatter must be a mapping')
    name = meta.get('name', '')
    require(name == 'somewhere-film', 'Unexpected skill name')
    require(bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name)), 'Invalid name')
    description = meta.get('description')
    require(isinstance(description, str) and 0 < len(description) <= 1024,
            'Description must be concise text')
    require('[TODO:' not in text, 'Unfinished skill scaffold')

    ui = yaml.safe_load((ROOT / 'agents/openai.yaml').read_text(encoding='utf-8'))
    interface = ui.get('interface', {})
    require('$' + name in interface.get('default_prompt', ''),
            'Default prompt must invoke this skill')
    require(25 <= len(interface.get('short_description', '')) <= 64,
            'UI short description needs 25–64 characters')
    require(bool(re.fullmatch(r'\d+\.\d+\.\d+\n?', (ROOT / 'VERSION').read_text())),
            'VERSION must contain a semantic version')

    files = source_files()
    for path in files:
        rel = path.relative_to(ROOT)
        require('.local' not in rel.parts, f'Local-only file tracked: {rel}')
        require(path.suffix.lower() not in MEDIA, f'Media file tracked: {rel}')
        require(path.is_file(), f'Tracked file is missing: {rel}')
        if path.suffix not in {'.md', '.yaml', '.yml', '.txt'}:
            continue
        content = path.read_text(encoding='utf-8')
        require(not re.search(r'/(?:Users|home)/[^/\s]+/', content),
                f'Personal absolute path found: {rel}')
        if path.suffix != '.md':
            continue
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
            u = urlsplit(link)
            if u.scheme or not u.path:
                continue
            target = (path.parent / unquote(u.path)).resolve()
            require(target.is_relative_to(ROOT), f'Link escapes repository: {link}')
            require(target.exists(), f'Broken reference in {rel}: {link}')
    print(f'PASS: skill metadata, UI, version, references and {len(files)} source files')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, yaml.YAMLError, subprocess.SubprocessError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
