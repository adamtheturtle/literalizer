module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_var : Val
my_var = RDict [
    ("_", RStr "_"),
    ]
my_data : Val
my_data = my_var
