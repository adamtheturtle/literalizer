module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "C:\\path\\to\\file",
    RStr "back\\\\slash",
    RStr "hello \\\"world\\\"",
    RStr "path\\to \"# file",
    RStr "trailing\\",
    RStr "both \"quotes''' here",
    RStr "line1\\nline2\nwith newline",
    ]
