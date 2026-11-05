module [my_data]

Val : [
    RBool Bool,
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("keep", RBool Bool.true),
    ("skip", RBool Bool.false),
]
