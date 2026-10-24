module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FStr "first line\n  indented\n\nlast line";
    FStr "\nleading newline";
    FStr " \t\nleading whitespace";
    FStr "trailing newline\n";
    FStr "\nleading and trailing\n";
    FStr "quotes: \"\"\" ''' ` and backslash: \\";
    FStr "interpolation: ${value} #{value} #@value #$value $value";
    FStr "backslash before newline: \\\nnext line";
    FStr "trailing spaces  \nnext";
    FStr "C++ empty delimiter collision: )\"\nvalue";
    FStr "C++ first fallback collision: )\" and )x\"\nvalue";
    FStr "C++ second fallback collision: )\" and )x\" and )x0\"\nvalue";
    FStr "Rust delimiter collision: \"#\nvalue";
    FStr "Lua delimiter collision: ]]\nvalue";
    FStr "Swift delimiter collision: \"\"\"#\nvalue";
    FStr "Swift interpolation collision: \\#(value)\nvalue";
    FStr "Ruby fallback interpolation  \n#{expression} #@instance #$global";
    FStr "NUL followed by a digit: \0007";
    FStr "carriage\rreturn"
]
