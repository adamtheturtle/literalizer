module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OStr "first line\n  indented\n\nlast line";
    OStr "\nleading newline";
    OStr " \t\nleading whitespace";
    OStr "trailing newline\n";
    OStr "\nleading and trailing\n";
    OStr "quotes: \"\"\" ''' ` and backslash: \\";
    OStr "interpolation: ${value} #{value} #@value #$value $value";
    OStr "backslash before newline: \\\nnext line";
    OStr "trailing spaces  \nnext";
    OStr "C++ empty delimiter collision: )\"\nvalue";
    OStr "C++ first fallback collision: )\" and )x\"\nvalue";
    OStr "C++ second fallback collision: )\" and )x\" and )x0\"\nvalue";
    OStr "Rust delimiter collision: \"#\nvalue";
    OStr "Lua delimiter collision: ]]\nvalue";
    OStr "Swift delimiter collision: \"\"\"#\nvalue";
    OStr "Swift interpolation collision: \\#(value)\nvalue";
    OStr "Ruby fallback interpolation  \n#{expression} #@instance #$global";
    OStr "NUL followed by a digit: \0007";
    OStr "carriage\rreturn"
]

end
