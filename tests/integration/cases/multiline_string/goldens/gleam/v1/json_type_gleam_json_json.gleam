import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("first line\n  indented\n\nlast line"),
    json.string("\nleading newline"),
    json.string(" \t\nleading whitespace"),
    json.string("trailing newline\n"),
    json.string("\nleading and trailing\n"),
    json.string("quotes: \"\"\" ''' ` and backslash: \\"),
    json.string("interpolation: ${value} #{value} #@value #$value $value"),
    json.string("backslash before newline: \\\nnext line"),
    json.string("trailing spaces  \nnext"),
    json.string("C++ empty delimiter collision: )\"\nvalue"),
    json.string("C++ first fallback collision: )\" and )x\"\nvalue"),
    json.string("C++ second fallback collision: )\" and )x\" and )x0\"\nvalue"),
    json.string("Rust delimiter collision: \"#\nvalue"),
    json.string("Lua delimiter collision: ]]\nvalue"),
    json.string("Swift delimiter collision: \"\"\"#\nvalue"),
    json.string("Swift interpolation collision: \\#(value)\nvalue"),
    json.string("Ruby fallback interpolation  \n#{expression} #@instance #$global"),
    json.string("NUL followed by a digit: \u{0000}7"),
    json.string("carriage\rreturn"),
  ])
  let _ = my_data
}
