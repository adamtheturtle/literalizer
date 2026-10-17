module [my_data]

Val : [
    JInt I128,
    JStr Str,
    JDict (List (Str, Val)),
]

my_data : Val
my_data = JDict [
    ("quote\"backslash\\", JInt 1i128),
    ("line\nbreak", JInt 2i128),
    ("\$(literal)\${text}", JInt 3i128),
    ("RStr prefix", JInt 4i128),
]
