from src.scanner import Scanner
from pathlib import Path


def parse_md(path):
    corrected_path = Path(path)
    with open(corrected_path, "r") as f:
        file_content = f.read()
        print(file_content)

    new_scanner = Scanner(file_content)
    root = new_scanner.tokenize()
    print(root)


def main():
    current_dir = Path(__file__).parent.resolve()
    parse_md(current_dir / "tests" / "test.md")


if __name__ == "__main__":
    main()
