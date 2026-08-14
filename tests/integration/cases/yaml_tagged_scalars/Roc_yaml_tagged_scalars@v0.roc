module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("explicit_string", RStr "5"),
    ("six", RStr "explicitly tagged key"),
    ]
