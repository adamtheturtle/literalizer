module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "first line\n  indented\n\nlast line",
    PStr "\nleading newline",
    PStr " \t\nleading whitespace",
    PStr "trailing newline\n",
    PStr "\nleading and trailing\n",
    PStr "quotes: \"\"\" ''' ` and backslash: \\",
    PStr "interpolation: ${value} #{value} #@value #$value $value",
    PStr "backslash before newline: \\\nnext line",
    PStr "trailing spaces  \nnext",
    PStr "C++ empty delimiter collision: )\"\nvalue",
    PStr "C++ first fallback collision: )\" and )x\"\nvalue",
    PStr "C++ second fallback collision: )\" and )x\" and )x0\"\nvalue",
    PStr "Rust delimiter collision: \"#\nvalue",
    PStr "Lua delimiter collision: ]]\nvalue",
    PStr "Swift delimiter collision: \"\"\"#\nvalue",
    PStr "Swift interpolation collision: \\#(value)\nvalue",
    PStr "Ruby fallback interpolation  \n#{expression} #@instance #$global",
    PStr "NUL followed by a digit: \x00\x37",
    PStr "carriage\rreturn"
]
