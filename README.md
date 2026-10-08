# atmcm1429.github.io
BBR Website

Display images live in `assets/images/`; the original uploads remain in their
existing folders. After replacing a photo or preview, rebuild the display copies:

```sh
python3 -m pip install Pillow
python3 scripts/optimize_images.py
```

For a new image, add its original path to `scripts/image_sources.json`, rebuild,
and reference its generated WebP file in the page. Portraits are cropped to the
same centered square used by the member cards. Logos keep their transparency.
