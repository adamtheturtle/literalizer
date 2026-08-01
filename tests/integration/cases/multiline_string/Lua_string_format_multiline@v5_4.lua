local my_data = {
    [[first line
  indented

last line]],
    "\nleading newline",
    [[trailing newline
]],
    "\nleading and trailing\n",
    [[quotes: """ ''' ` and backslash: \]],
    [[interpolation: ${value} #{value} #@value #$value $value]],
    [[backslash before newline: \
next line]],
    "trailing spaces  \nnext",
    [[C++ delimiter collision: )LITERALIZER"
value]],
    [[Rust delimiter collision: "#
value]],
    [=[Lua delimiter collision: ]]
value]=],
    "Ruby fallback interpolation  \n#{expression} #@instance #$global",
    "NUL followed by a digit: \x007",
    "carriage\rreturn",
}
