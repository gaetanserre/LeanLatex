#let config(doc) = {
  set raw(
    theme: "catppuccin_latte.thTheme",
    syntaxes: "lean4.sublime-syntax",
  )

  set page(width: auto, height: auto, margin: 1pt)

  show raw: set text(font: ("FiraCode Nerd Font", "JuliaMono"))

  show raw.where(block: true): block.with(
    fill: rgb("#f6f8fa"),
    inset: 5pt,
    radius: 5pt,
    stroke: 0.5pt + rgb("#d0d7de"),
  )

  doc
}
