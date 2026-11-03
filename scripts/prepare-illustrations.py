"""Encode generated PNGs as web assets without changing their composition.

Usage: python scripts/prepare-illustrations.py path/to/local-inputs.json
Input entries contain slug, title, labels, alt, and source_path. Install Pillow
only when preparing assets; the website has no Python or image-library runtime.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', type=Path)
    parser.add_argument('--out', default='assets/illustrations')
    parser.add_argument('--style', choices=['skeuomorphic', 'flat'], default='skeuomorphic')
    args = parser.parse_args()
    inputs = json.loads(args.inputs.read_text(encoding='utf-8-sig'))
    out = (ROOT / args.out).resolve()
    assert out.is_relative_to(ROOT), 'Asset directory must be in this repository'
    out.mkdir(parents=True, exist_ok=True)
    originals = ROOT / '.preview/illustration-originals' / args.style
    originals.mkdir(parents=True, exist_ok=True)
    manifest = []
    for item in inputs:
        source = Path(item['source_path'])
        slug = item['slug']
        shutil.copy2(source, originals / f'{slug}.png')
        target = out / f'{slug}.webp'
        with Image.open(source) as picture:
            picture.save(target, format='WEBP', quality=90, method=6)
            width, height = picture.size
        manifest.append({
            'slug': slug, 'title': item['title'], 'labels': item['labels'],
            'alt': item['alt'], 'width': width, 'height': height,
            'representation': args.style + '-system-illustration',
            'source': 'Built-in image_gen; explanatory visual metaphor',
            'source_type': item.get('source_type', 'project-or-paper-description'),
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'file': target.relative_to(ROOT).as_posix(),
            'bytes': target.stat().st_size,
        })
        schematic = ROOT / f'assets/models/{slug}.svg'
        if schematic.is_file():
            manifest[-1]['technical_schematic'] = schematic.relative_to(ROOT).as_posix()
    (out / 'manifest.json').write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8'
    )
    total = sum(item['bytes'] for item in manifest)
    print(f'Prepared {len(manifest)} illustrations, {total / 1024:.0f} KiB total.')


if __name__ == '__main__':
    main()
