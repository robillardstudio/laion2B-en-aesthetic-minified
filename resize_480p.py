"""
Resize LAION images to 480p.

Resizes every image in images/ so it fits within a 854x480 bounding box
(preserving aspect ratio, no upscaling) and writes the results to
images_480p/. Originals in images/ are left untouched. Images at or
below 480p height are copied through unresized, so the image list in
images/ and images_480p/ stays the same.
"""

from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

from PIL import Image
from tqdm import tqdm

SRC_DIR = Path("images")
DST_DIR = Path("images_480p")
MAX_W, MAX_H = 854, 480   # bounding box for 480p
UPSCALE = False             # leave smaller images as-is
JPEG_QUALITY = 90


def resize_one(src_path_str):
    src_path = Path(src_path_str)
    dst_path = DST_DIR / src_path.name

    try:
        with Image.open(src_path) as im:
            im = im.convert("RGB")  # drop alpha / normalize mode for JPEG output
            w, h = im.size

            if h > MAX_H:
                scale = min(MAX_W / w, MAX_H / h)
                if not UPSCALE:
                    scale = min(scale, 1.0)

                if scale != 1.0:
                    new_size = (max(1, round(w * scale)), max(1, round(h * scale)))
                    im = im.resize(new_size, Image.LANCZOS)

            im.save(dst_path, "JPEG", quality=JPEG_QUALITY)
        return (src_path.name, True, None)
    except Exception as e:
        return (src_path.name, False, str(e))


def main():
    DST_DIR.mkdir(exist_ok=True)

    image_paths = sorted(SRC_DIR.glob("*.jpg"))
    print(f"Found {len(image_paths)} images in {SRC_DIR}/")

    errors = []
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(resize_one, str(p)) for p in image_paths]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Resizing"):
            name, ok, err = future.result()
            if not ok:
                errors.append((name, err))

    print(f"Done. {len(image_paths) - len(errors)} succeeded, {len(errors)} failed.")
    if errors:
        print("First few errors:")
        for name, err in errors[:10]:
            print(f"  {name}: {err}")


if __name__ == "__main__":
    main()
