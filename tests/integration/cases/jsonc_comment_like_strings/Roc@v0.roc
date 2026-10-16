module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "// data",
    RStr "/* data */",
    RStr "escaped quote: \" // data",
    RStr "backslash: \\",
]
