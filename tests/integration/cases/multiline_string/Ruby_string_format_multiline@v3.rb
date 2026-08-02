my_data = [
  'first line
  indented

last line',
  '
leading newline',
  " \t\nleading whitespace",
  'trailing newline
',
  '
leading and trailing
',
  'quotes: """ \'\'\' ` and backslash: \\',
  'interpolation: ${value} #{value} #@value #$value $value',
  'backslash before newline: \\
next line',
  "trailing spaces  \nnext",
  'C++ delimiter collision: )LITERALIZER"
value',
  'Rust delimiter collision: "#
value',
  'Lua delimiter collision: ]]
value',
  'Swift delimiter collision: """#
value',
  'Swift interpolation collision: \\#(value)
value',
  "Ruby fallback interpolation  \n\#{expression} \#@instance \#$global",
  "NUL followed by a digit: \x007",
  "carriage\rreturn",
]
