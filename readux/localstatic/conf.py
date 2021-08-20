from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static_local",
]

STATIC_ROOT = BASE_DIR.parent / "static_cdn" / "static_root"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / "static_cdn" / "media_root"

PROTECTED_ROOT = BASE_DIR.parent / "static_cdn" / "protected_media"