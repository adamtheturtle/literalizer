module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "first line\n  indented\n\nlast line",
    EStr "\nleading newline",
    EStr " \t\nleading whitespace",
    EStr "trailing newline\n",
    EStr "\nleading and trailing\n",
    EStr "quotes: \"\"\" ''' ` and backslash: \\",
    EStr "interpolation: ${value} #{value} #@value #$value $value",
    EStr "backslash before newline: \\\nnext line",
    EStr "trailing spaces  \nnext",
    EStr "C++ empty delimiter collision: )\"\nvalue",
    EStr "C++ first fallback collision: )\" and )x\"\nvalue",
    EStr "C++ second fallback collision: )\" and )x\" and )x0\"\nvalue",
    EStr "Rust delimiter collision: \"#\nvalue",
    EStr "Lua delimiter collision: ]]\nvalue",
    EStr "Swift delimiter collision: \"\"\"#\nvalue",
    EStr "Swift interpolation collision: \\#(value)\nvalue",
    EStr "Ruby fallback interpolation  \n#{expression} #@instance #$global",
    EStr "NUL followed by a digit: \u{0000}7",
    EStr "carriage\rreturn"
    ]
