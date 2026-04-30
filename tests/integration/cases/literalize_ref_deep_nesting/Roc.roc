module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("a", RDict [("b", RDict [("c", RDict [("$ref", RStr "deep")])])]),
    ]
