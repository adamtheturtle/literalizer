module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("x", RStr "\u(0000)"),
    ("y", RStr "\u(0000)1"),
    ]
