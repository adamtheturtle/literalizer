my_data = (
    r'''first line
  indented

last line''',
    r'''
leading newline''',
    " \t\nleading whitespace",
    r'''trailing newline
''',
    r'''
leading and trailing
''',
    "quotes: \"\"\" ''' ` and backslash: \\",
    r"interpolation: ${value} #{value} #@value #$value $value",
    r'''backslash before newline: \
next line''',
    "trailing spaces  \nnext",
    r'''C++ empty delimiter collision: )"
value''',
    r'''C++ first fallback collision: )" and )x"
value''',
    r'''C++ second fallback collision: )" and )x" and )x0"
value''',
    r'''Rust delimiter collision: "#
value''',
    r'''Lua delimiter collision: ]]
value''',
    r'''Swift delimiter collision: """#
value''',
    r'''Swift interpolation collision: \#(value)
value''',
    "Ruby fallback interpolation  \n#{expression} #@instance #$global",
    "NUL followed by a digit: \x007",
    "carriage\rreturn",
)
