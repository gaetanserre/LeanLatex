## Code LaTeX preprocessor

This repository contains a LaTeX preprocessor for code blocks. It allows you to write code in your LaTeX documents and automatically processes it to generate the graphics.

### Requirements

- [Typst](https://typst.app/) (to render code blocks to PDF)

### Usage

Install the preprocessor by using the following command:

```bash
pip install .
```

In your LaTeX document, you can include code using the following syntax:

```latex
\begin{code}{lean}[width=\textwidth,height=\textheight] % or any options for \includegraphics
import Mathlib
example : StrictMono (fun (x : ℝ) ↦ x + 1) := by
  intro x y hxy
  /-
    x y : ℝ
    hxy : x < y
    ⊢ x + 1 < y + 1
  -/
  exact (add_lt_add_iff_right 1).mpr hxy
\end{code}
```

Then, run the preprocessor on your LaTeX file:

```bash
code_latex your_document.tex
```

It will generate `your_document.tex_processed.tex` with the code replaced by the corresponding graphics:

```latex
\includegraphics[width=\textwidth,height=\textheight]{figures/codeblocks/code-block-0.pdf}
```

It is easy to create a custom LaTeX command to include the processed file in your main document.

#### Font size option

You can specify a custom font size for the generated graphics by adding the `fontsize` option to the `code` environment. For example:

```latex
\begin{code}{lean}[fontsize=10pt]
...
\end{code}
```

### Numbering option

You can enable line numbering in the generated graphics by adding the `numbering` option to the `code` environment. For example:

```latex
\begin{code}{lean}[numbering=1]
...
\end{code}
```

This option will be passed to the Typst template, allowing you to customize the font size of the rendered code in the generated graphics.

### Customization

You can customize the output directory for the generated graphics by modifying the Typst template in `code_latex/figures/template.typ`.

### License

This project is under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.