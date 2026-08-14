module [my_data]

Val : [
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_var : Val
my_var = RInt 1i128
my_data : Val
my_data = RDict [
    ("key", my_var),
    ]
