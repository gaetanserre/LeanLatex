## Lean LaTeX preprocessor

This repository contains a LaTeX preprocessor for Lean code. It allows you to write Lean code in your LaTeX documents and automatically processes it to generate the graphics.

### Requirements
- [Typst](https://typst.app/) (to render Lean code to PDF)

### Usage

Install the preprocessor by using the following command:

```bash
pip install .
```

In your LaTeX document, you can include Lean code using the following syntax:

```latex
\begin{leancode}[width=\textwidth,height=\textheight] % or any options for \includegraphics
import Mathlib
example : StrictMono (fun (x : ℝ) ↦ x + 1) := by
  intro x y hxy
  /-
    x y : ℝ
    hxy : x < y
    ⊢ x + 1 < y + 1
  -/
  exact (add_lt_add_iff_right 1).mpr hxy
\end{leancode}
```

Then, run the preprocessor on your LaTeX file:

```bash
lean_latex your_document.tex
```

It will generate `your_document.tex_processed.tex` with the Lean code replaced by the corresponding graphics:

```latex
\includegraphics[width=\textwidth,height=\textheight]{figures/leanblocks/lean-block-0.pdf}
```

It is easy to create a custom LaTeX command to include the processed file in your main document.

### Customization
You can customize the output directory for the generated graphics by modifying the Typst template in `lean_latex/figures/template.typ`.

### License
This project is under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.