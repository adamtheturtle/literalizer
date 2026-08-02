val my_data = arrayOf(
    """first line
  indented

last line""",
    """
leading newline""",
    " \t\nleading whitespace",
    """trailing newline
""",
    """
leading and trailing
""",
    """quotes: ${'"'}${'"'}${'"'} ''' ` and backslash: \""",
    """interpolation: ${'$'}{value} #{value} #@value #${'$'}value ${'$'}value""",
    """backslash before newline: \
next line""",
    "trailing spaces  \nnext",
    """C++ empty delimiter collision: )${'"'}
value""",
    """C++ first fallback collision: )${'"'} and )x${'"'}
value""",
    """C++ second fallback collision: )${'"'} and )x${'"'} and )x0${'"'}
value""",
    """Rust delimiter collision: ${'"'}#
value""",
    """Lua delimiter collision: ]]
value""",
    "Ruby fallback interpolation  \n#{expression} #@instance #\$global",
    "NUL followed by a digit: \u00007",
    "carriage\rreturn",
)
