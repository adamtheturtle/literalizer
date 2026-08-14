module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

a_b_c : Val
a_b_c = RDict [
    ("_", RStr "_"),
    ]
my_data : Val
my_data = a_b_c
