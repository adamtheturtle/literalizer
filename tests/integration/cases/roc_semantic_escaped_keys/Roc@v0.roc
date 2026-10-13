module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("quote\"backslash\\", RInt 1i128),
    ("line\nbreak", RInt 2i128),
    ("\$(literal)\${text}", RInt 3i128),
    ("RStr prefix", RInt 4i128),
]
