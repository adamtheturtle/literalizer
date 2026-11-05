module [my_data]

Val : [
    RBool Bool,
    RInt I128,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("keep", RBool Bool.true),
    ("skip", RInt 0i128),
]
