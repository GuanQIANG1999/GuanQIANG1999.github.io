"""Encode generated PNGs as web assets without changing their composition.

Usage: python scripts/prepare-illustrations.py path/to/local-inputs.json
Input entries contain slug, title, labels, alt, and source_path. Install Pillow
only when preparing assets; the website has no Python or image-library runtime.
"""
from pathlib import Path
import hashlib
import json
import shutil
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/illustrations'


def main():
    inputs = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'))
    OUT.mkdir(parents=True, exist_ok=True)
    originals = ROOT / '.preview/illustration-originals'
    originals.mkdir(parents=True, exist_ok=True)
    manifest = []
    for item in inputs:
        source = Path(item['source_path'])
        slug = item['slug']
        shutil.copy2(source, originals / f'{slug}.png')
        target = OUT / f'{slug}.webp'
        with Image.open(source) as picture:
            picture.save(target, format='WEBP', quality=90, method=6)
            width, height = picture.size
        manifest.append({
            'slug': slug, 'title': item['title'], 'labels': item['labels'],
            'alt': item['alt'], 'width': width, 'height': height,
            'representation': 'skeuomorphic-system-illustration',
            'source': 'Built-in image_gen; explanatory visual metaphor',
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'file': f'assets/illustrations/{slug}.webp',
            'technical_schematic': f'assets/models/{slug}.svg',
            'bytes': target.stat().st_size,
        })
    (OUT / 'manifest.json').write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8'
    )
    total = sum(item['bytes'] for item in manifest)
    print(f'Prepared {len(manifest)} illustrations, {total / 1024:.0f} KiB total.')


if __name__ == '__main__':
    main()
