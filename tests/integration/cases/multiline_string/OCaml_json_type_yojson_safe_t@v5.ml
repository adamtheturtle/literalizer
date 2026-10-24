module Check = struct

let my_data : Yojson.Safe.t = `List [
    `String "first line\n  indented\n\nlast line";
    `String "\nleading newline";
    `String " \t\nleading whitespace";
    `String "trailing newline\n";
    `String "\nleading and trailing\n";
    `String "quotes: \"\"\" ''' ` and backslash: \\";
    `String "interpolation: ${value} #{value} #@value #$value $value";
    `String "backslash before newline: \\\nnext line";
    `String "trailing spaces  \nnext";
    `String "C++ empty delimiter collision: )\"\nvalue";
    `String "C++ first fallback collision: )\" and )x\"\nvalue";
    `String "C++ second fallback collision: )\" and )x\" and )x0\"\nvalue";
    `String "Rust delimiter collision: \"#\nvalue";
    `String "Lua delimiter collision: ]]\nvalue";
    `String "Swift delimiter collision: \"\"\"#\nvalue";
    `String "Swift interpolation collision: \\#(value)\nvalue";
    `String "Ruby fallback interpolation  \n#{expression} #@instance #$global";
    `String "NUL followed by a digit: \0007";
    `String "carriage\rreturn"
]

end
