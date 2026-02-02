import argparse
import subprocess
from pathlib import Path

wd = Path(__file__).parent.resolve()
diff_lines = 0


def cli():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("doc", type=str, help="LaTeX document to parse.")

    args = parser.parse_args()
    return args


def file_exists(filepath):
    try:
        with open(filepath, "r"):
            return True
    except FileNotFoundError:
        return False


def parse_options(option_str):
    option_str = (option_str[1:-1]).split(",")
    options = {}
    if option_str == [""]:
        return options
    for option in option_str:
        key, value = option.split("=")
        options[key.strip()] = value.strip()
    return options


def find_lean_blocks(latex_content):
    lean_blocks = []
    lines = latex_content.splitlines()
    inside_lean_block = False
    current_block = []

    for i, line in enumerate(lines):
        if line.strip().startswith(r"\begin{leancode}"):
            inside_lean_block = True
            current_block = []
            start = i
            options = parse_options(line.strip()[len(r"\begin{leancode}") :])
        elif line.strip().startswith(r"\end{leancode}"):
            inside_lean_block = False
            lean_blocks.append(
                {
                    "start": start,
                    "end": i,
                    "options": options,
                    "content": "\n".join(current_block),
                }
            )
        elif inside_lean_block:
            current_block.append(line)

    return lean_blocks, lines


def create_figure(lean_block, i, output_dir):
    typst_content = f"""
    #import "template.typ": *

    #show: doc => config(doc)

    #align(center, box(
      [
```lean4
{lean_block['content']}
```
      ],
    ))
    """
    with open(f"{wd}/figures/lean-block-{i}.typ", "w") as f:
        f.write(typst_content)

    subprocess.run(
        [
            "typst",
            "compile",
            f"{wd}/figures/lean-block-{i}.typ",
            f"{output_dir}/lean-block-{i}.pdf",
        ]
    )


def insert_figure_in_latex(lines, lean_block, i):
    options = ",".join(
        [f"{key}={value}" for key, value in lean_block["options"].items()]
    )
    graphics = (
        f"\\includegraphics[{options}]{{figures/leanblocks/lean-block-{i}.pdf}}".split(
            "\n"
        )
    )
    global diff_lines

    lines[lean_block["start"] - diff_lines : lean_block["end"] + 1 - diff_lines] = (
        graphics
    )
    # update diff_lines
    diff_lines += (lean_block["end"] - lean_block["start"] + 1) - len(graphics)


def clean():
    # remove all files in figures/
    figures_dir = wd / Path("figures")
    for file in figures_dir.iterdir():
        if file.name.startswith("lean-block-"):
            file.unlink()


def main():
    args = cli()
    if not file_exists(args.doc):
        raise FileNotFoundError(f"The file {args.doc} does not exist.")
    with open(args.doc, "r") as f:
        latex_content = f.read()
    lean_blocks, lines = find_lean_blocks(latex_content)
    output_dir = Path(args.doc).parent.resolve() / "figures" / "leanblocks"
    output_dir.mkdir(exist_ok=True, parents=True)
    for i, lean_block in enumerate(lean_blocks):
        create_figure(lean_block, i, output_dir)
        insert_figure_in_latex(lines, lean_block, i)
    new_latex_content = "\n".join(lines)
    output_file = Path(args.doc).name + "_processed.tex"
    with open(Path(args.doc).parent / output_file, "w") as f:
        f.write(new_latex_content)
    clean()


if __name__ == "__main__":
    main()
