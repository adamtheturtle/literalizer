module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    # strings stay data
    RStr "https://example.org/a/*b*/",  # URL annotation
    RStr "escaped quote: \" // still data",
    RStr "backslash: \\",  # outside the string
    RStr "/* not a comment */",
]
