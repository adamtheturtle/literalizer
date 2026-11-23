pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("first line\n  indented\n\nlast line"),
    GStr("\nleading newline"),
    GStr(" \t\nleading whitespace"),
    GStr("trailing newline\n"),
    GStr("\nleading and trailing\n"),
    GStr("quotes: \"\"\" ''' ` and backslash: \\"),
    GStr("interpolation: ${value} #{value} #@value #$value $value"),
    GStr("backslash before newline: \\\nnext line"),
    GStr("trailing spaces  \nnext"),
    GStr("C++ empty delimiter collision: )\"\nvalue"),
    GStr("C++ first fallback collision: )\" and )x\"\nvalue"),
    GStr("C++ second fallback collision: )\" and )x\" and )x0\"\nvalue"),
    GStr("Rust delimiter collision: \"#\nvalue"),
    GStr("Lua delimiter collision: ]]\nvalue"),
    GStr("Swift delimiter collision: \"\"\"#\nvalue"),
    GStr("Swift interpolation collision: \\#(value)\nvalue"),
    GStr("Ruby fallback interpolation  \n#{expression} #@instance #$global"),
    GStr("NUL followed by a digit: \u{0000}7"),
    GStr("carriage\rreturn"),
  ])
  let _ = my_data
}
