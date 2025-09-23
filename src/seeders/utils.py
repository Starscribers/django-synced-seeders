from pathlib import Path

from django.conf import settings


def get_seed_meta_path() -> Path:
    if hasattr(settings, "SEEDS_META_PATH"):
        seed_path = Path(settings.SEEDS_META_PATH)
    else:
        seed_path = Path(settings.BASE_DIR) / "seeds_meta.json"

    seed_path.parent.mkdir(parents=True, exist_ok=True)

    if not seed_path.exists():
        with seed_path.open("w") as file:
            file.write("{}\n")

    return seed_path
