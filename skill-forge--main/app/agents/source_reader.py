
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ALLOWED_DIRECTORIES = {
    "api",
    "agents",
    "ai",
    "business",
    "database",
    "models",
    "repositories",
    "schemas",
    "security",
    "services",
    "utils",
}

MAX_FILES = 12
MAX_FILE_CHARS = 5000


def read_project_sources(question: str) -> str:
    """
    Read relevant Python source files from SkillForge.

    Only searches approved application directories.
    Does not read .env files, virtual environments,
    database files, or arbitrary files outside app/.
    """
    question_words = {
        word.lower().strip(".,?!():")
        for word in question.split()
        if len(word) > 2
    }

    candidates = []

    for directory in ALLOWED_DIRECTORIES:
        folder = PROJECT_ROOT / "app" / directory

        if not folder.is_dir():
            continue

        for path in folder.glob("*.py"):
            if path.name == "__init__.py":
                continue

            filename_words = set(
                path.stem.lower().replace("-", "_").split("_")
            )

            score = len(question_words & filename_words)

            if score > 0:
                candidates.append((score, path))

    main_file = PROJECT_ROOT / "app" / "main.py"

    if main_file.is_file():
        candidates.append((0, main_file))

    candidates.sort(key=lambda item: item[0], reverse=True)

    results = []
    seen = set()

    for _, path in candidates:
        if path in seen:
            continue

        seen.add(path)

        try:
            content = path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except OSError:
            continue

        relative_path = path.relative_to(PROJECT_ROOT)
        content = content[:MAX_FILE_CHARS]

        results.append(
            f"\n--- Source file: {relative_path} ---\n"
            f"{content}"
        )

        if len(results) >= MAX_FILES:
            break

    if not results:
        return "No matching source files were found."

    return "\n".join(results)