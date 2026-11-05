module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    # first dotted key
    # second dotted key
    ("a", RDict [("b", RInt 1i128), ("c", RInt 2i128)]),
]
