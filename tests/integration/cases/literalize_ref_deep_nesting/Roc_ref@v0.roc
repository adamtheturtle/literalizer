module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

deep : Val
deep = RDict [
    ("_", RStr "_"),
    ]
my_data : Val
my_data = RDict [
    ("a", RDict [("b", RDict [("c", deep)])]),
    ]
