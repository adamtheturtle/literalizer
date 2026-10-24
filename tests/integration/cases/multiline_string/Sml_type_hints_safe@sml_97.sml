datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "first line\n  indented\n\nlast line",
    SStr "\nleading newline",
    SStr " \t\nleading whitespace",
    SStr "trailing newline\n",
    SStr "\nleading and trailing\n",
    SStr "quotes: \"\"\" ''' ` and backslash: \\",
    SStr "interpolation: ${value} #{value} #@value #$value $value",
    SStr "backslash before newline: \\\nnext line",
    SStr "trailing spaces  \nnext",
    SStr "C++ empty delimiter collision: )\"\nvalue",
    SStr "C++ first fallback collision: )\" and )x\"\nvalue",
    SStr "C++ second fallback collision: )\" and )x\" and )x0\"\nvalue",
    SStr "Rust delimiter collision: \"#\nvalue",
    SStr "Lua delimiter collision: ]]\nvalue",
    SStr "Swift delimiter collision: \"\"\"#\nvalue",
    SStr "Swift interpolation collision: \\#(value)\nvalue",
    SStr "Ruby fallback interpolation  \n#{expression} #@instance #$global",
    SStr "NUL followed by a digit: \0007",
    SStr "carriage\rreturn"
]
val _ = my_data
