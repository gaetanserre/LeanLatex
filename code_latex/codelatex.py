import argparse
import subprocess
import re
from pathlib import Path

wd = Path(__file__).parent.resolve()
diff_lines = 0
dict_fig = {}


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


def find_code_blocks(latex_content):
    code_blocks = []
    lines = latex_content.splitlines()
    inside_code_block = False
    current_block = []
    begin_pattern = re.compile(r"^\\begin\{code\}\{([^}]*)\}(\[.*\])?$")

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        begin_match = begin_pattern.match(stripped_line)
        if begin_match:
            inside_code_block = True
            current_block = []
            start = i
            language = begin_match.group(1).strip()
            options = parse_options(begin_match.group(2) or "[]")
        elif stripped_line.startswith(r"\end{code}"):
            inside_code_block = False
            code_blocks.append(
                {
                    "start": start,
                    "end": i,
                    "language": language,
                    "options": options,
                    "content": "\n".join(current_block),
                }
            )
        elif inside_code_block:
            current_block.append(line)

    return code_blocks, lines


def create_figure(code_block, i, output_dir):
    font_size = code_block["options"].get("fontsize", "7pt")
    numbering = bool(int(code_block["options"].get("numbering", "0")))

    if numbering:
        show_raw_line = '#show raw.line: it => [#text(fill: rgb("#aaaaaa"), if it.count >= 10 and it.number < 10 { " " + str(it.number) } else { str(it.number) } ) #it]'
    else:
        show_raw_line = ""

    if code_block["content"] not in dict_fig:
        typst_content = f"""
#import "template.typ": *

#show: doc => config(doc)

#show raw: set text(size: {font_size})

{show_raw_line}

```{code_block['language']}
{code_block['content']}
```
      """
        with open(f"{wd}/figures/code-block-{i}.typ", "w") as f:
            f.write(typst_content)

        subprocess.run(
            [
                "typst",
                "compile",
                f"{wd}/figures/code-block-{i}.typ",
                f"{output_dir}/code-block-{i}.pdf",
            ]
        )

        # Remove all parents of output_dir until we reach the "figures" directory
        full_path = Path(f"{output_dir}/code-block-{i}.pdf")
        parts = full_path.parts
        try:
            figures_index = parts.index("figures")
            relative_path = Path(*parts[figures_index:])
        except ValueError:
            # If "figures" is not in the path, use the full path
            relative_path = full_path

        dict_fig[code_block["content"]] = str(relative_path)


def insert_figure_in_latex(lines, code_block):
    code_block["options"].pop("fontsize", None)
    code_block["options"].pop("numbering", None)

    options = ",".join(
        [f"{key}={value}" for key, value in code_block["options"].items()]
    )
    fig = dict_fig[code_block["content"]]
    graphics = f"\\includegraphics[{options}]{{{fig}}}".split("\n")
    global diff_lines

    lines[code_block["start"] - diff_lines : code_block["end"] + 1 - diff_lines] = (
        graphics
    )
    # update diff_lines
    diff_lines += (code_block["end"] - code_block["start"] + 1) - len(graphics)


def clean():
    # remove all files in figures/
    figures_dir = wd / Path("figures")
    for file in figures_dir.iterdir():
        if file.name.startswith("code-block-"):
            file.unlink()


def main():
    args = cli()
    if not file_exists(args.doc):
        raise FileNotFoundError(f"The file {args.doc} does not exist.")
    with open(args.doc, "r") as f:
        latex_content = f.read()
    code_blocks, lines = find_code_blocks(latex_content)
    if code_blocks != []:
        output_dir = Path(args.doc).parent.resolve() / "figures" / "codeblocks"
        # delete all existing files in output_dir
        if output_dir.exists():
            for file in output_dir.iterdir():
                file.unlink()
            output_dir.rmdir()
        output_dir.mkdir(exist_ok=True, parents=True)
        for i, code_block in enumerate(code_blocks):
            create_figure(code_block, i, output_dir)
            insert_figure_in_latex(lines, code_block)
    new_latex_content = "\n".join(lines)
    output_file = Path(args.doc).name + "_processed.tex"
    with open(Path(args.doc).parent / output_file, "w") as f:
        f.write(new_latex_content)
    clean()


if __name__ == "__main__":
    main()
