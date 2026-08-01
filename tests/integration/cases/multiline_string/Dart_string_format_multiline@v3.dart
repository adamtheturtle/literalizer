final my_data = <String>[
    '''first line
  indented

last line''',
    '''\nleading newline''',
    ''' \t\nleading whitespace''',
    '''trailing newline
''',
    '''\nleading and trailing
''',
    '''quotes: """ \'\'\' ` and backslash: \\''',
    '''interpolation: \${value} #{value} #@value #\$value \$value''',
    '''backslash before newline: \\
next line''',
    '''trailing spaces\x20\x20
next''',
    '''C++ delimiter collision: )LITERALIZER"
value''',
    '''Rust delimiter collision: "#
value''',
    '''Lua delimiter collision: ]]
value''',
    '''Ruby fallback interpolation\x20\x20
#{expression} #@instance #\$global''',
    '''NUL followed by a digit: \x007''',
    '''carriage\rreturn''',
];
