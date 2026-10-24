module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "first line\n  indented\n\nlast line",
    RStr "\nleading newline",
    RStr " \t\nleading whitespace",
    RStr "trailing newline\n",
    RStr "\nleading and trailing\n",
    RStr "quotes: \"\"\" ''' ` and backslash: \\",
    RStr "interpolation: \${value} #{value} #@value #$value $value",
    RStr "backslash before newline: \\\nnext line",
    RStr "trailing spaces  \nnext",
    RStr "C++ empty delimiter collision: )\"\nvalue",
    RStr "C++ first fallback collision: )\" and )x\"\nvalue",
    RStr "C++ second fallback collision: )\" and )x\" and )x0\"\nvalue",
    RStr "Rust delimiter collision: \"#\nvalue",
    RStr "Lua delimiter collision: ]]\nvalue",
    RStr "Swift delimiter collision: \"\"\"#\nvalue",
    RStr "Swift interpolation collision: \\#(value)\nvalue",
    RStr "Ruby fallback interpolation  \n#{expression} #@instance #$global",
    RStr "NUL followed by a digit: \u(0000)7",
    RStr "carriage\rreturn",
]
